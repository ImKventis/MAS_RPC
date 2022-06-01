# SubMod framework
A simple framework has been implimented to allow other mods to set the activity on the fly

further help can be found by DMing KvenAltis#6716 (GMT Timezone) and I will be happy to explain further


# Functions

## set_act(details: str, room: str, icon: str)

```python
store.kventis_rpc.set_act(details, room, icon)
```

Allows submods to set activity via code rather than waiting for ch30-minute

Details: this is the section of the RPC that usally says "Spending time with monika"

Room: the room Monika is currently in leave as None for current

Icon: Icon to use, None for users preference

### Examples

```python
store.kventis_rpc.set_act('Booping {monika}', None, 'def')
```

This will set the RPC to a rich pressence saying "Booping [monika nickname]" with whatever room the user is currently in and the default icon

Whichh looks like this

<img src="https://imgur.com/j6ykigb.jpg" style="padding-bottom:20px;padding-top:20px">


```python
store.kventis_rpc.set_act('Chilling out', None, None)
```

This will set the RPC to "Chilling out" with current room and current user selected icon


## block_for(minutes: int)

```python
store.kventis_rpc.block_for(minutes)
```

Blocks the minutly update for set ammount of minutes which can be useful after a set_act to prevent it from being overwritten almost instantly

### Examples

```python
store.kventis_rpc.block_for(3)
```

This will prevent the auto update for 3 minutes


# Jsons

If you provide custom rooms or custom "be right back messages" a json map will be better than manually setting the activity.

Jsons live under "rpc/maps", in this folder is 2 folders called "b" and "r".

b - be right back messages JSONS

r - room JSONS

## Be right back json map

```json
{
    "brb_eating_callback": ["Eating with {monika}", "Enjoying a meal with {monika}"],
    "brb_watching_movie_callback": "Watching a movie with {monika}"
}
```

The be right back json takes a idle callback label as the key and the value should the message for the status. {monika} will be replaced with monikas nickname at update time

keys can be lists of strings to be randomly picked from at update time or single strings.

## Room json map

```json
{
    "submod_office": "In the fancy office building",
    "submod_80s_restrant": "In a old restrant"
}
```
This json takes a room ID as the key and the value as the text to replace "In the Spaceroom"