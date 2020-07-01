"""
Checkout system which takes item codes as input, applies
the discount and generates final bill with total price
"""
import argparse
from collections import Counter
from prettytable import PrettyTable

class CalculatePrice:
    """
    Base class to take user items and provide a view of applied discount
    and the final price for the items
    """
    def __init__(self):
        self.price_dict = {'CH1':3.11, 'AP1':6.00, 'CF1':11.23, 'MK1':4.75, 'OM1':3.69}
        self.bill_info = PrettyTable(['Item', 'Discount Applied', 'Price'])
        self.discount_token, self.discount_amount, self.price = '', 0, 0
        self.total_items, self.flag = [], False

    def check_item(self, item):
        """
        Gets the price of each item and formulates bill as per the applied discount
        """
        self.total_items.append(item)
        self.bill_info.add_row([item, '', self.price_dict[item]])
        self.price = self.price + self.price_dict[item]
        if len(self.total_items) > 1:
            self.apply_discount()
            if self.flag is True:
                self.bill_info.add_row(['', self.discount_token, -self.discount_amount])
        self.bill_info.add_row(['', '', round(self.price, 2)])
        print(self.bill_info)

    def apply_discount(self):
        """
        Checks if any of the four discounts apply on the items till current point
        """
        self.flag = False
        count = dict(Counter(self.total_items))

        #Checks for discount BOGO
        if 'CF1' in count.keys():
            if count['CF1'] % 2 == 0:
                self.discount_amount = (count['CF1']/2)*self.price_dict['CF1']
                self.price = self.price - self.discount_amount
                self.flag = True
            else:
                self.discount_amount = (int(count['CF1']/2)*self.price_dict['CF1'])
                self.price = self.price - self.discount_amount
                self.flag = True
            self.discount_token = 'BOGO'

        #Checks for discount APPL
        if 'AP1' in count.keys():
            if count['AP1'] == 3 and self.total_items[-1] == 'AP1':
                self.price = self.price - 4.50
                self.discount_token, self.discount_amount = 'APPL', 4.50
                self.flag = True

        #Checks for discount CHMK
        if 'CH1' in count.keys() and 'MK1' in count.keys():
            if count['MK1'] == 1:
                self.price = self.price - self.price_dict['MK1']
                self.discount_token, self.discount_amount = 'CHMK', self.price_dict['MK1']
                self.flag = True

        #Checks for discount APOM
        if 'OM1' in count.keys() and self.total_items[-1] == 'OM1':
            if count['OM1'] > 1:
                last_occ = max(loc for loc, val in enumerate(self.total_items) if val == 'OM1')
                temp_list = self.total_items[last_occ:-1]
                if 'AP1' in temp_list:
                    new_count = temp_list.count('AP1')
                    self.discount_amount = (self.price_dict['AP1']*new_count)/2
                    self.price, self.discount_token = self.price - self.discount_amount, 'APOM'
                    self.flag = True
            elif 'AP1' in count.keys():
                self.discount_amount = (self.price_dict['AP1']*count['AP1'])/2
                self.price, self.discount_token = self.price - self.discount_amount, 'APOM'
                self.flag = True

    def main(self):
        """
        Takes command line input of items and calls necessary methods for
        checking applicable discounts. Prints the final price along with the bill.
        """
        print('Welcome to Farmer Market!\nBelow are products available and price.')
        items_info = PrettyTable(['Product Code', 'Name', 'Price'])
        items_info.add_row(['CH1', 'Chai', '$3.11'])
        items_info.add_row(['AP1', 'Apples', '$6.00'])
        items_info.add_row(['CF1', 'Coffee', '$11.23'])
        items_info.add_row(['MK1', 'Milk', '$4.75'])
        items_info.add_row(['OM1', 'Oatmeal', '$3.69'])
        print(items_info)
        print('\n\nBelow is the discount information.\n \
        BOGO -- Buy-One-Get-One-Free Special on Coffee. (Unlimited)\n \
        APPL -- If you buy 3 or more bags of Apples, the price drops to $4.50.\n \
        CHMK -- Purchase a box of Chai and get milk free. (Limit 1)\n \
        APOM -- Purchase a bag of Oatmeal and get 50% off a bag of Apple\n\n')

        parser = argparse.ArgumentParser()
        parser.add_argument('-i','--items', nargs='+', help='Item codes', required=True, choices=['CH1', 'AP1', 'CF1', 'MK1', 'OM1'])
        args = parser.parse_args()
        print('Provided basket items - {}'.format(args.items))
        for item in args.items:
            self.check_item(item)
            self.bill_info.del_row(-1)
        print('Final Price: {}'.format(round(self.price, 2)))

if __name__ == '__main__':
    CalculatePrice().main()
