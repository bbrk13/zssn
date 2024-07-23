# ZSSN
Zombie Survival Social Network

## General Information

#### Problem Description
ZSSN (Zombie Survival Social Network). The world as we know it has fallen into an apocalyptic scenario. A laboratory-made virus is transforming human beings and animals into zombies, hungry for fresh flesh.

You, as a zombie resistance member (and the last survivor who knows how to code), was designated to develop a system to share resources between non-infected humans.

## Features

- **Add survivors to the database**: A survivor must have a _name_, _age_, _gender_, and _last location (latitude, longitude)_. A survivor also has an inventory of resources of their own property (which you need to declare upon the registration of the survivor).

- **Update survivor location**: A survivor must have the ability to update their last location, storing the new latitude/longitude pair in the base (no need to track locations, just replacing the previous one is enough).

- **Flag survivor as infected**: In a chaotic situation like that, it's inevitable that a survivor may get contaminated by the virus. When this happens, we need to flag the survivor as infected. An infected survivor cannot trade with others, can't access/manipulate their inventory, nor be listed in the reports (infected people are kinda dead anyway). A survivor is marked as infected when at least three other survivors report their contamination. When a survivor is infected, their inventory items become inaccessible (they cannot trade with others).

- **Survivors cannot Add/Remove items from inventory**: Their belongings must be declared when they are first registered in the system. After that, they can only change their inventory by means of trading with other survivors.

- **Trade items**: Survivors can trade items among themselves. To do that, they must respect the price table below, where the value of an item is described in terms of points. Both sides of the trade should offer the same amount of points. For example, 1 Water and 1 Medication (1 x 4 + 1 x 2) is worth 6 ammunition (6 x 1) or 2 Food items (2 x 3). The trades themselves need not be stored, but the items must be transferred from one survivor to the other.




Item   ->      Points

1 Water      -> 4 points

1 Food     ->  3 points

1 Medication -> 2 points

1 Ammunition -> 1 point


## Technical Information

- **Frontend**: VueJS with Vuetify framework
- **Backend**: Python Django with Rest Framework
- **Endpoints**: 
  - `api/trade_offers/`
  - `api/survivors`
- **Database**: MySQL 5.7

## How to Run

The entire system runs on Docker. Use the following Makefile commands:

- `make open`: Open and run the project
- `make repopen`: Clear all caches and run the project