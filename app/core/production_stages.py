STAGES = [
    {
        "id": 1,
        "name": "Recepção",
    },
    {
        "id": 2,
        "name": "Design",
    },
    {
        "id": 3,
        "name": "Impressão",
    },
    {
        "id": 4,
        "name": "Estamparia",
    },
    {
        "id": 5,
        "name": "Costura",
    },
    {
        "id": 6,
        "name": "Entrega",
    },
]


FIRST_STAGE = STAGES[0]

LAST_STAGE = STAGES[-1]

def get_stage(stage_name: str):

    for stage in STAGES:

        if stage["name"] == stage_name:
            return stage

    return None

def get_stage_names():

    return [
        stage["name"]
        for stage in STAGES
    ]

def get_stage_index(stage_name: str):

    names = get_stage_names()

    return names.index(stage_name)

def get_next_stage(stage_name: str):

    index = get_stage_index(stage_name)

    if index >= len(STAGES) - 1:
        return None

    return STAGES[index + 1]["name"]

def get_previous_stage(stage_name: str):

    index = get_stage_index(stage_name)

    if index <= 0:
        return None

    return STAGES[index - 1]["name"]

def get_allowed_moves(stage_name: str):

    moves = []

    previous = get_previous_stage(stage_name)

    if previous:
        moves.append(previous)

    moves.append(stage_name)

    next_stage = get_next_stage(stage_name)

    if next_stage:
        moves.append(next_stage)

    return moves