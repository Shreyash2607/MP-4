import cv2
import numpy
import toupcam


class TouptekExampleApp:
    def __init__(self):
        self.hcam = None
        self.buf = None
        self.total = 0

    # the vast majority of callbacks come from toupcam.dll/so/dylib internal threads
    @staticmethod
    def on_camera_event(event, ctx):
        if event == toupcam.TOUPCAM_EVENT_IMAGE:
            ctx.handle_image_event()

    def handle_image_event(self):
        try:
            self.hcam.PullImageV2(self.buf, 24, None)
            self.total += 1
            print('pull image ok, total = {}'.format(self.total))
            self._save_color_frame()
        except toupcam.HRESULTException:
            print('pull image failed')

    def _save_color_frame(self):
        raw_bgr_array = numpy.array(bytearray(self.buf))
        raw_rgb_array = raw_bgr_array[..., ::-1].copy()
        mono_image = raw_rgb_array.reshape(1080, 1920, 3)
        cv2.imwrite('frames/frame%s.bmp' % self.total, mono_image)

    def run(self):
        a = toupcam.Toupcam.EnumV2()
        if len(a) > 0:
            print('{}: flag = {:#x}, preview = {}, still = {}'.format(
                a[0].displayname, a[0].model.flag, a[0].model.preview, a[0].model.still)
            )
            for r in a[0].model.res:
                print('\t = [{} x {}]'.format(r.width, r.height))
            self.hcam = toupcam.Toupcam.Open(a[0].id)
            if self.hcam:
                try:
                    width, height = self.hcam.get_Size()
                    bufsize = ((width * 24 + 31) // 32 * 4) * height
                    print('image size: {} x {}, bufsize = {}'.format(width, height, bufsize))
                    self.buf = bytes(bufsize)
                    if self.buf:
                        try:
                            self.hcam.StartPullModeWithCallback(self.on_camera_event, self)
                        except toupcam.HRESULTException:
                            print('failed to start camera')
                    input('press ENTER to exit')
                finally:
                    self.hcam.Close()
                    self.hcam = None
                    self.buf = None
            else:
                print('failed to open camera')
        else:
            print('no camera found')


if __name__ == '__main__':
    app = TouptekExampleApp()
    app.run()