
from dash_spa.components import StateWrapper

# Minimal TODO model

TODO_MODEL= {
    "past": [],
    "todo": [],
    "future": []
    }

class ModelActions:

    def add(state, input):
        """Add todo entry"""
        current = state.todo.copy()
        state.past.append(current)
        state.todo.append(input)
        state.future = []
        return state

    def delete(state, index):
        """Delete todo entry"""
        state.past.append(state.todo.copy())
        state.todo.pop(index)
        return state

    def undo(state):
        """undo last action"""
        if len(state.past) > 0:
            state.future.append(state.todo)
            state.todo = state.past.pop()
        return state

    def redo(state):
        """redo last action"""
        if len(state.future) > 0:
            state.past.append(state.todo)
            state.todo = state.future.pop()
        return state

def can_undo(state):
    state = StateWrapper(state)
    return len(state.past) > 0

def can_redo(state):
    state = StateWrapper(state)
    return len(state.future) > 0
