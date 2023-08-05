import numpy as np
import matplotlib.pyplot as plt
from .frame_stream import FrameStream
import ipywidgets as widgets
from ipywidgets import interact


class FART:

    def __init__(self, filename=None, gridfs=None, recording_software='fart'):
        if filename:
            self._FrameStream = FrameStream(filename=filename)
        elif gridfs:
            self._FrameStream = FrameStream(gridfs=gridfs)
        else:
            raise ValueError('Needs at least one argument, filename or gridfs')

    @property
    def measurement_info(self):
        return self._FrameStream.measurement_info

    @property
    def time(self):
        return self._FrameStream.time

    @property
    def frames(self):
        return self._FrameStream

    def show_frames_as_video(self):
        out = widgets.Output()
        play = widgets.Play(
            value=0,
            min=0,
            max=len(self.time) - 1,
            step=1,
            description="Press play",
            disabled=False
        )
        slider = widgets.IntSlider(
            value=0,
            min=0,
            max=len(self.time) - 1,
            step=1,
            description='Time:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
        )
        interact(self._plot_frame_with_index, index=play)
        widgets.jslink((play, 'value'), (slider, 'value'))
        widgets.VBox([slider, out])

    def get_frame_at_time(self, time):
        return self._FrameStream.get_frame_at_time(time)

    def plot_frame_at_time(self, time):
        frame = self.get_frame_at_time(time)
        self._plot_frame(frame)

    def plot_all_frames(self, figsize=(6, 8)):
        plt.style.use({'figure.figsize': figsize})
        interact(self.plot_frame_at_time, time=widgets.SelectionSlider(
            options=self.time,
            value=self.time[0],
            description='Time:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True
        ))

    @staticmethod
    def _find_index_of_nearest(array, value):
        return (np.abs(np.array(array) - value)).argmin()

    @staticmethod
    def _plot_frame(frame):
        plt.imshow(frame)

    def _plot_frame_with_index(self, index):
        frame = self.frames[index]
        self._plot_frame(frame)
