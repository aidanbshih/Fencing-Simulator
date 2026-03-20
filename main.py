from dataclasses import dataclass, field
from enum import Enum, auto

PISTE_LENGTH = 14.0  # meters
CENTER = 7.0
WARNING_LINE_LEFT = 2.0
WARNING_LINE_RIGHT = 12.0

position: float # meters from left end, clamped [0.0, 14.0]

class Stance(Enum):
    EN_GARDE    = auto() # all other actions are available
    ADVANCING   = auto()
    RETREATING  = auto()
    LUNGING     = auto() # fencer is committed and cannot change action until recovery begins. 
    FLECHE      = auto() # irreversible -- fencer must pass the opponent
    IN_RECOVERY = auto() # prevent double-actions

class BladePosition(Enum):
    # each of the four parries corresponds to a quadrant of target that the
    # fencer can force the opponent's blade out of.
    SIXTE    = auto()
    QUARTE   = auto()
    OCTAVE   = auto()
    SEPTIME  = auto()
    # Engagement / absence of blade:
    ENGAGED  = auto()  # blade-to-blade contact without a parry
    ABSENCE  = auto()  # no blade contact (in absence of blade)

class ActionState(Enum):
    IDLE              = auto()  # no committed action
    ATTACKING         = auto()  # arm extended, point threatening target
    PARRYING          = auto()
    RIPOSTING         = auto()
    COUNTER_ATTACING = auto()
    FLECHING          = auto()
    BEATING           = auto()

@dataclass
class Fencer:
    # Identity
    name: str

    # Position on piste
    position: float           # meters from left end [0.0, 14.0]

    # Movement / posture
    stance: Stance = Stance.EN_GARDE

    # Blade
    blade_position: BladePosition = BladePosition.ABSENCE

    # Current action
    action_state: ActionState = ActionState.IDLE

    # Right-of-way
    has_priority: bool = False

    # Scoring
    score: int = 0
    yellow_cards: int = 0
    red_cards: int = 0
    black_card: bool = False

    # Lockout / touch timing
    time_on_target: float = 0.0   # seconds; reset each phrase

    def is_expelled(self) -> bool:
        return self.black_card

    def penalty_touch_count(self) -> int:
        """Each red card donates 1 touch to the opponent."""
        return self.red_cards