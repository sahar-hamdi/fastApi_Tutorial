from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel


app = FastAPI()
@app.get("/")
async def root():
    return {"message" : "Hello World"}


@app.post("/")
async def post():
    return {"message" : "This is the post request"}


@app.put("/", description = "this is a put endpoint")
async def put():
    return {"message" : "This is the put request"}


@app.get("/users")
async def list_users():
    return {"message" : "this is a users list"}

# to make the user with id 1 is to be  the admin
# FasetAPI byshof el requests wl endpoints el 3ndo bl trteb fa 3lshan
# kda lw 3ndy two methods by3mlo nfs el haga t2rebn yb2a akhly 
# el static method fl awl w el dynamic b3dha


# if I need to disappear the user admin request form the doc 
# we add include_in_schema = False to the get parameters
#  @app.get("/users/1", include_in_schema = False)
@app.get("/users/1")
async def admin_user():
    return {"message" : "this is the admin portal"}

@app.get("/users/{user_id}")
async def get_user(user_id : int):
    return {"user_id" : user_id}

class User_List(str, Enum):
    admin = 1
    manager = 2
    user = 3

@app.get("/{user_type}/{user_id}")
async def get_user_type(user_type : User_List, user_id):
    return {"user" : {user_type.name, user_id}}


#query parameters

items = [
    {"id":1 , "name":"book" , "price":"15" , "stock": True},
    {"id":2 , "name":"game" , "price":"50" , "stock": True},
    {"id":3 , "name":"cd" , "price":"30" , "stock": True},
    {"id":4 , "name":"magazine" , "price":"10" , "stock": False},
    {"id":5 , "name":"book" , "price":"10" , "stock": True},
    {"id":6 , "name":"game" , "price":"10" , "stock": True}
]

@app.get("/items")
async def list_items(
    start : int = 0,
    end : int = 10,
    id : int = None,
    name : str = None
):
    if id:
        item = next((item for item in items if item["id"] == id), None)
        if item:
            return item
        
        else:
            return {"message" : "item not found"}

    if name:
        filtered = []
        for item in items:
            if item["name"] == name:
                filtered.append(item)
        return filtered

    return items[start : start + end]


@app.get("/items/prices")
async def sort_price(range : int = None):
    sorted_price = sorted(items , key= lambda x:x["price"] , reverse=True)

    if range:
        price_range = [item for item in sorted_price if item["price"] <= str(range)]

        return price_range
    else:
        return sorted_price


@app.get("/items/stock")
async def get_stock(in_stock:bool = True):
    if not in_stock:
        item = [item for item in items if item["stock"] == False]

        return item
    else:
        item = [item for item in items if item["stock"] == True]
        return item



class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : float | None = None

@app.post("/items")
async def create_item(item: Item):
    return item