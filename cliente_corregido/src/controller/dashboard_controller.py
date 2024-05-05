##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: dashboard_controller.py
# Capitulo: Flujo de Datos
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís
# Version: 1.0.0 Noviembre 2022
# Descripción:
#
#   Este archivo define la funcionalidad del componente
#
#-------------------------------------------------------------------------
from datetime import datetime
from src.data.repository import Repository
import json

class DashboardController:

    @staticmethod
    def load_products():
        response = Repository.get_products()
        if response.status_code != 200:
            return {"products": 0} 
        
        json_response = json.loads(response.text)

        assert('data' in json_response.keys())
        assert('response' in json_response['data'].keys())

        return {
            "products": json_response["data"]["response"][0]["count"]
        }

    @staticmethod
    def load_providers():
        response = Repository.get_providers()
        if response.status_code != 200:
            return {"providers": 0}
        
        json_response = json.loads(response.text)

        assert('data' in json_response.keys())
        assert('response' in json_response['data'].keys())

        return {
            "providers": json_response["data"]["response"][0]["count"]
        }

    @staticmethod
    def load_locations():
        response = Repository.get_locations()
        if response.status_code != 200:
            return {"locations": 0}
        
        json_response = json.loads(response.text)

        assert('data' in json_response.keys())
        assert('response' in json_response['data'].keys())

        return {
            "locations": json_response["data"]["response"][0]["count"]
        }

    @staticmethod
    def load_orders():
        response = Repository.get_orders()
        if response.status_code != 200:
            return {"orders": 0}
        
        json_response = json.loads(response.text)

        assert('data' in json_response.keys())
        assert('response' in json_response['data'].keys())

        return {
            "orders": json_response["data"]["response"][0]["count"]
        }

    @staticmethod
    def load_sales():
        response = Repository.get_sales()
        if response.status_code != 200:
            return {"sales": 0}
        
        json_response = json.loads(response.text)
        
        assert('data' in json_response.keys())
        assert('response' in json_response['data'].keys())

        return {
            "sales": json_response["data"]["response"][0]["total"]
        }

    @staticmethod
    def load_providers_per_location():
        response = Repository.get_providers_by_location()
        if response.status_code != 200:
            return {
                "providers": [],
                "location": []
            }
        result = {
            "providers": [],
            "location": []
        }

        json_response = json.loads(response.text)

        assert('data' in json_response.keys())
        assert('response' in json_response['data'].keys())

        for entry in json_response["data"]["response"]:
            result["providers"].append(entry["providers"][0]["count"])
            result["location"].append(entry["name"])
        return result

    @staticmethod
    def load_sales_per_location():
        response = Repository.get_sales_by_location()
        if response.status_code != 200:
            return {
                "sales": [],
                "location": []
            }
        result = {
            "sales": [],
            "location": []
        }
        json_response = json.loads(response.text)

        assert('data' in json_response.keys())
        assert('response' in json_response['data'].keys())

        for entry in json_response["data"]["response"]:
            result["location"].append(entry["name"])
            total = 0
            for sold in entry["providers"]:
                for order in sold["sold"]:
                    total += (int(order["quantity"]) * float(order["quantity"]))
            result["sales"].append(total)
            
        return result

    @staticmethod
    def load_orders_per_location():
        response = Repository.get_orders_by_location()
        if response.status_code != 200:
            return {
                "orders": [],
                "location": []
            }
        result = {
            "orders": [],
            "location": []
        }
        json_response = json.loads(response.text)

        assert('data' in json_response.keys())
        assert('response' in json_response['data'].keys())

        for entry in json_response["data"]["response"]:
            result["location"].append(entry["name"])
            total = 0
            for sold in entry["providers"]:
                total += int(sold["sold"])
            result["orders"].append(total)
        return result

    @staticmethod
    def load_best_sellers():
        response = Repository.get_best_sellers()
        if response.status_code != 200:
            return []
        result = []
        json_response = json.loads(response.text)

        assert('data' in json_response.keys())
        assert('response' in json_response['data'].keys())

        for product in json_response["data"]["response"][0:5]:
            result.append({
                "invoice": product["times"],
                "total": int(product["times"]) * float(product["price"]),
            })
        return result

    @staticmethod
    def load_worst_sales():
        response = Repository.get_worst_sales()
        if response.status_code != 200:
            return []
        result = []
        json_response = json.loads(response.text)

        assert('data' in json_response.keys())
        assert('response' in json_response['data'].keys())

        for product in json_response["data"]["response"][0:5]:
            result.append({
                "invoice": product["times"],
                "total": int(product["times"]) * float(product["price"])
            })
        return result

    @staticmethod
    def load_most_selled_products():
        response = Repository.get_most_selled_products()
        if response.status_code != 200:
            return []
        result = []
        json_response = json.loads(response.text)

        assert('data' in json_response.keys())
        assert('response' in json_response['data'].keys())

        for product in json_response["data"]["response"][0:5]:
            result.append({
                "product": product["description"],
                "times": product["times"]
            })
        return result
    
    @staticmethod
    def load_sales_per_date(start_date_str, end_date_str):
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        response = Repository.get_sales_per_period()
        if response.status_code != 200:
            return []
        
        result = []
        json_response = json.loads(response.text)

        assert('data' in json_response.keys())
        assert('response' in json_response['data'].keys())

        for sale in json_response["data"]["response"]:
            sale_date = datetime.strptime(sale["date"], "%Y-%m-%dT%H:%M:%SZ").date()
            if start_date <= sale_date <= end_date:
                result.append({
                    "date": sale["date"],
                    "product": sale["product"],
                    "total_price": sale["product"][0]["price"]
                    
                })
        return result
    

    @staticmethod
    def load_product_per_date(start_date_str, end_date_str):
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        response = Repository.get_product_per_period()
        if response.status_code != 200:
            return []
        
        result = []
        json_response = json.loads(response.text)

        assert('data' in json_response.keys())
        assert('response' in json_response['data'].keys())
        
        sorted_sales = sorted(json_response["data"]["response"], key=lambda x: x["product"][0]["times"], reverse=True)

        for sale in sorted_sales:
            sale_date = datetime.strptime(sale["date"], "%Y-%m-%dT%H:%M:%SZ").date()
            if start_date <= sale_date <= end_date:

                product_info = {
                    "date": sale["date"],
                    "quantity": sale["quantity"],
                    "total": sale["total"],
                    "description": sale["product"][0]["description"],
                    "times": sale["product"][0]["times"]
                }
                # If the product is not already in the result list, add it
                if product_info not in result:
                    result.append(product_info)

        return result

