#!/usr/bin/python
# -*- coding: utf-8 -*-
from Homevee.Item import Item
from Homevee.Item.ShoppingListItem import ShoppingListItem


def get_shopping_list(user, db):
    items = ShoppingListItem.load_all(db)
    return {'Item': ShoppingListItem.list_to_dict(items)}

def add_edit_shopping_list_item(user, id, amount, name, db):
    shopping_list_item = Item.load_from_db(ShoppingListItem, id)
    if shopping_list_item is None:
        shopping_list_item = ShoppingListItem(name, amount, id)
    else:
        shopping_list_item.amount = amount
        shopping_list_item.name = name

    return shopping_list_item.api_save()

def delete_shopping_list_item(user, id, db):
    item = Item.load_from_db(ShoppingListItem, id, db)
    return item.api_delete()