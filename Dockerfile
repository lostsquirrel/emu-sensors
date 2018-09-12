FROM registry.cn-hangzhou.aliyuncs.com/lisong/python-base:0.1.0

ADD ./ /app
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /app/requirements.txt
EXPOSE 9093

ENTRYPOINT [ "python", "/app/application.py" ]