FROM python:3.6.0

ADD generate_bill.py /
ADD README.md /

RUN pip install prettytable

ENTRYPOINT [ "python", "./generate_bill.py" ]
