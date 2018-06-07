

def base_dialog():
  dialog = {
    "directed": True,
    "multigraph": False,
    "name": "Dialog",
    "nodes": [
        {
            "name": "root",
            "id": "node0"
        },
        {
            "name": "riddle 1",
            "id": "node1"
        },
        {
            "name": "joke 1",
            "id": "node2"
        }
    ],
    "links": [
        {
            "source": 0,
            "target": 1,
            "command": "Tell me ? riddle",
            "response": "What's black and white and read all over.",
            "value": 1
        },
        {
            "source": 0,
            "target": 2,
            "command": "Tell me ? joke",
            "response": "A large number of mathematicians walk into a bar. The first one orders a beer, the second orders half a beer, the third orders a quarter of a glass of beer. Before the 4th mathematician can say anything the bartender slams 2 beers on the bar and says that's all you're getting. You women need to learn your limits.",  # noqa
            "value": 2
        },
        {
            "source": 1,
            "target": 0,
            "command": "* newspaper *",
            "response": "You got it!",
            "value": 3
        }
    ]
}
  return dialog
