from dataclasses import dataclass
from typing import Union, Tuple
import io
from logging import getLogger


TrackType = Union[str, io.BufferedIOBase]


@dataclass
class Music:
    name: str
    track: TrackType = None

    def __eq__(self, other):
        return self.name == other.name


class Queue:
    _queue = []

    def on_track_finish(self, err, requeue_on_err=True):
        if err:
            pass
            # logger.error("Could not play the track", err)
        # if not err or (err and not requeue_on_err):
        #     del self._queue[0]

    def next(self, cursor=0) -> Music:
        return self._queue[cursor] if cursor < len(self._queue) else None

    def __len__(self) -> int:
        return len(self._queue)

    @property
    def size(self):
        return self.__len__()

    @property
    def queue(self):
        return self._queue

    def add(self, music: Music):
        self._queue.append(music)

    def remove(self, music: Music) -> None:
        del self._queue[self._queue.index(music)]

    def retrieve(self, music: Music = None):
        if not Music.name:
            raise IndexError
        return next((music for music in self._queue if music.name == music.name), None)

    def skip(self, cursor) -> Music:
        return self._queue[cursor]
