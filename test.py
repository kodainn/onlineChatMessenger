import threading

import ctypes
import time

# カスタムスレッドクラス
class twe(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        threading.Thread.__init__(self, group=group, target=target, name=name)
        self.args = args
        self.kwargs = kwargs
        return
    
    def run(self):
        self._target(*self.args, **self.kwargs)

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
    
    # 強制終了させる関数
    def raise_exception(self):
        thread_id = self.get_id()
        resu = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), ctypes.py_object(SystemExit))
        if resu > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), 0)
            print('Failure in raising exception')

# 開始するスレッドで実行する関数
def sample_func(a, b, c, hoge1 = None, hoge2 = None, hoge3 = None):
    try:
        while True:
            print((a, b, c, hoge1, hoge2, hoge3))
            time.sleep(1)
    finally:
          print('ended')

def main():
    # 開始するスレッドを定義
    # targetに実行する関数
    # args, kwargsには関数に渡す引数
    x = twe(name = 'Thread A', target=sample_func, args=(1, 2, 3), kwargs={'hoge1': 'hogehoge1', 'hoge2': 'hogehoge2', 'hoge3': 'hogehoge3'})
    # スレッド開始
    x.start()
    # 10秒間、開始したスレッドが処理し続ける
    time.sleep(10)
    # raise_exceptionを呼び出すことでスレッドが終了
    x.raise_exception()
    # 既に終了しているので処理を待機しないはず
    x.join()

if __name__ == '__main__':
    main() 