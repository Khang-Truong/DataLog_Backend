from typing import Collection
import motor.motor_asyncio
from models.model import Wastage


client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://DataLog:DataLog@cluster0.jzr1zc7.mongodb.net/test')
database = client.DataLog
collection = database.Wastage


async def fetch_all_wastage():
    wastages = []
    cursor = collection.aggregate([ 
                                    {'$group': {"_id" : "$Product_Name", "Total_Quantity": {"$sum": "$Quantity"}   }},
                                    {'$sort': {"Total_Quantity": -1}},
                                    {'$limit': 10}
                                ])
    async for document in cursor:
        wastages.append(document)
    return wastages

async def fetch_date_range_wastage(start_date,end_date):
    wastages = []
    cursor = collection.aggregate([ {'$match': {'Date': { "$gte": start_date, "$lte":  end_date} }},
                                    {'$group': {"_id" : "$Product_Name", "Total_Quantity": {"$sum": "$Quantity"}   }},
                                    {'$sort': {"Total_Quantity": -1}},
                                    {'$limit': 10}
                                ])
    async for document in cursor:
        wastages.append(document)
    return wastages



