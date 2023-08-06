#!/usr/bin/python
# -*- coding: utf-8 -*-
from Homevee.Item import Item
from Homevee.Item.ShoppingListItem import ShoppingListItem
from Homevee.Utils.Database_NEW import Database


def get_shopping_list(user, db: Database = None):
    if db is None:
        db = Database()
    items = ShoppingListItem.load_all(db)
    return ShoppingListItem.list_to_dict(items)

def add_edit_shopping_list_item(user, id, amount, name, db: Database = None):
    if db is None:
        db = Database()
    shopping_list_item = Item.load_from_db(ShoppingListItem, id, db)
    if shopping_list_item is None:
        shopping_list_item = ShoppingListItem(name, amount, id)
    else:
        shopping_list_item.amount = amount
        shopping_list_item.name = name

    return shopping_list_item.api_save()

def delete_shopping_list_item(user, id, db: Database = None):
    if db is None:
        db = Database()
    item = Item.load_from_db(ShoppingListItem, id, db)
    return item.api_delete()