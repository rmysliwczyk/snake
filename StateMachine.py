class StateMachine:
    current_state = None
    @classmethod
    def change_current(cls, state):
        cls.current_state = state

    @classmethod
    def update_current(cls, clock):
        cls.current_state.update(clock)
    
    @classmethod
    def draw_current(cls):
        cls.current_state.draw()