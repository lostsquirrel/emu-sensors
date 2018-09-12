import tornado.ioloop
import tornado.web
import os
import psutil


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.add_header("Content-Type", "text/plain;charset=utf-8")
        self.write(format_prometheus())


def get_temperatures():
    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures()
    else:
        temps = {}

    return temps


def get_fans():
    if hasattr(psutil, "sensors_fans"):
        fans = psutil.sensors_fans()
    else:
        fans = {}

    return fans


def format_prometheus():
    pp = ''
    temps = get_temperatures()
    for k, v in temps.items():
        k = k.upper()
        for index, x in enumerate(v):
            if len(x[0]) > 0:
                index = x[0].replace(" ", "_").upper()
            pp += '%s_%s_TEMP %s\n' % (k, index, x[1])
            pp += '%s_%s_TEMP_HIGH %s\n' % (k, index, x[2])
            pp += '%s_%s_TEMP_CRITICAL %s\n' % (k, index, x[3])

    return pp


application = tornado.web.Application([
    (r"/metrics", MainHandler),

])
if __name__ == "__main__":
    port = os.environ.get("PORT")
    if port is None:
        port = 9093
    application.listen(int(port))
    tornado.ioloop.IOLoop.instance().start()
