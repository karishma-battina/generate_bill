# generate_bill/checkout system

Below are the instructions to run 'generate_bill.py' file

#python generate_bill.py -i itemcode1 itemcode2

#Example: python generate_bill.py -i AP1 CH1

-----------------------------
Command Line Arguments
-----------------------------
1. File 'generate_bill.py' should be executed by passing command line arguments.
Arguments should be space separated item codes.

2. The input arguments will be validated to ensure that invalid arguments
are not passed.

-------------------------------
Design
-------------------------------
The script is implemented to get the total price along with discounts applied at any
specific point.

All the items added will be validated for any applicable discount and will proceed
further with the total price calculation.


Limitation: Removal of item is not possible once added, if the command line argument
is invalid, the execution will be terminated.

------------------------------
Docker
------------------------------
The Dockerfile should be built and running of the image starts the python script in
a container.

#docker build -t price-image .
#docker run price-image -i AP1 CH1
