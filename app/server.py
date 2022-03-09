import aiohttp
import asyncio
import uvicorn
import soundfile as sf
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import librosa.display
import librosa
from fastai import *
from fastai.vision.all import *
import pathlib
import sys
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

export_file_url = 'https://www.dropbox.com/s/dbmsf8oumi0en60/model_spec_three.pkl?dl=1'
export_file_name = 'export1.pkl'
temp = pathlib.PosixPath
#pathlib.PosixPath = pathlib.WindowsPath
from starlette.routing import Route

classes = ['black', 'grizzly', 'teddys']

path = pathlib.Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))


async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f:
                f.write(data)


async def setup_learner():
    await download_file(export_file_url, path / export_file_name)
    try:
        import pathlib
        full_path = os.path.join(path, export_file_name)
        learn = load_learner(full_path)
        # learn = load_learner(path.parent,  export_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()


@app.route('/')
async def homepage(request):
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open(encoding='utf8').read())


@app.route('/analyze', methods=['POST'])
async def analyze(request):
    audio_data = await request.form()
    audio_bytes = await (audio_data['file'].read())
    y, sr = sf.read(BytesIO(audio_bytes))
    sf.write('new_file.wav', y, sr)

    y,sr=librosa.load('new_file.wav')
    print(y.shape,sr)
    y = y[:100000]

    window_size = 1024
    window = np.hanning(window_size)
    stft  = librosa.core.spectrum.stft(y, n_fft=window_size, hop_length=512, window=window)
    out = 2 * np.abs(stft) / np.sum(window)

    #fig = plt.Figure()
    fig = plt.figure(figsize=(800/144, 800/144), dpi=144)
    ax = fig.add_subplot(111)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)
    ax.set_aspect('equal')

    canvas = FigureCanvas(fig)
    p = librosa.display.specshow(librosa.amplitude_to_db(out, ref=np.max), ax=ax, y_axis='log', x_axis='time')
    plt.savefig('output.png', dpi =144, bbox_inches='tight',pad_inches=0)
    import cv2
    image = cv2.imread('output.png')


    return JSONResponse({'result': str(learn.predict(image))})


if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
