import time
import subprocess
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC


# todo: firefox preference permissions.default.microphone 1

@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    return chrome_options


def _exec(command, timeout: int | None = None):
    process = subprocess.Popen(command, shell=True)
    try:
        process.wait(timeout)
    except subprocess.TimeoutExpired:
        process.kill()


def play_through_mic(filename: str):
    # playing an audio file through mic sink makes Pulseaudio server to stream it through virtual source associated
    # with that sink (see pulse.cfg), in other words simulating speech
    _exec(f"paplay --device=mic {filename}")


def record_speakers(output: str, timeout: int):
    # you can add extra encoding parameters here, like --rate=8000 --channels=1 --format=ulaw
    _exec(f"pacat --file-format=wav -r -d speaker.monitor > {output}",
          timeout=timeout)


def test_voice(selenium):
    wait = WebDriverWait(selenium, 30)
    selenium.get("https://online-voice-recorder.com/")

    record_btn = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "btn-record")))
    record_btn.click()

    for _ in range(5):
        play_through_mic("hello-world.wav")
        time.sleep(1)

    stop_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="btn-record active"]')))
    stop_btn.click()

    play_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "play-button")))
    play_btn.click()

    record_speakers("/artifacts/speakers.wav", 10)

