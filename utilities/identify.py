import time
import aiohttp
import asyncio
import threading
import numpy as np
import tensorflow as tf
import concurrent.futures

_interpreter_pool = []
_prediction_cache = {}

_labels = eval(open("source/names.txt", "r").read())

_executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)
_interpreter_lock = threading.Lock()

_cache_lock = threading.Lock()
_cache_timeout = 300

def initialize_pool(num_interpreters=8):
    global _interpreter_pool
    _interpreter_pool = [_initialize_interpreter() for _ in range(num_interpreters)]

def _initialize_interpreter():
    interpreter = tf.lite.Interpreter(model_path="source/pokefire.tflite")
    interpreter.allocate_tensors()
    return interpreter

def _remove_alpha_channel(image):
    return image[:, :, :3]

def _preprocess_input_image(image):
    img = tf.image.resize(image, [224, 224]) / 255.0
    return img

async def _prepare_image_for_prediction(image_url):
    with _cache_lock:
        if image_url in _prediction_cache:
            cache_entry = _prediction_cache[image_url]
            if time.time() - cache_entry["timestamp"] < _cache_timeout:
                return cache_entry["data"], True

    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            image_data = await response.read()

    image = tf.image.decode_image(image_data, channels=3).numpy()
    preprocessed_image = _preprocess_input_image(image)

    return preprocessed_image, False

async def predict_pokemon_from_url(image_url):
    preprocessed_data, is_cached = await _prepare_image_for_prediction(image_url)

    if is_cached:
        return preprocessed_data

    with _interpreter_lock:
        if not _interpreter_pool:
            interpreter = _initialize_interpreter()
        else:
            interpreter = _interpreter_pool.pop()

    try:
        predicted_pokemon = await asyncio.get_event_loop().run_in_executor(
            _executor,
            _predict_pokemon_sync,
            interpreter,
            preprocessed_data.numpy() if not is_cached else preprocessed_data,
        )

        with _cache_lock:
            _prediction_cache[image_url] = {
                "data": predicted_pokemon,
                "timestamp": time.time(),
            }
            _clean_cache()

        return predicted_pokemon
    finally:
        with _interpreter_lock:
            _interpreter_pool.append(interpreter)

def _clean_cache():
    now = time.time()
    expired_keys = [
        key
        for key, value in _prediction_cache.items()
        if now - value["timestamp"] > _cache_timeout
    ]
    for key in expired_keys:
        del _prediction_cache[key]

def _predict_pokemon_sync(interpreter, image):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    input_data = tf.convert_to_tensor([image], dtype=tf.float32)
    interpreter.set_tensor(input_details[0]["index"], input_data)

    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]["index"])
    prediction_scores = output_data[0]

    predictions = [
        (_labels[i], round(score * 100, 1))
        for i, score in enumerate(prediction_scores)
    ]
    predictions.sort(key=lambda x: x[1], reverse=True)
    return predictions[:3]
