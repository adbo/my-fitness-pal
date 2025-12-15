"""
Exercise data with progression chains.

Each progression chain contains exercises ordered from easiest to hardest.
Users progress by mastering each exercise before moving to the next.
"""

from ..models import Exercise, MuscleGroup, DifficultyLevel, ProgressionChain


# =============================================================================
# PUSH-UP PROGRESSION
# Wall → Counter → Knee → Full → Diamond → Archer → One-arm
# =============================================================================

PUSH_UP_PROGRESSION = ProgressionChain(
    id="pushup",
    name="Push-up Progression",
    name_pl="Progresja Pompek",
    description="Progress from wall push-ups to one-arm push-ups",
    exercises=[
        Exercise(
            id="pushup_wall",
            name="Wall Push-ups",
            name_pl="Pompki od ściany",
            description="Stand facing a wall, place hands on wall at shoulder height, perform push-up motion.",
            muscle_groups=[MuscleGroup.CHEST, MuscleGroup.TRICEPS, MuscleGroup.SHOULDERS],
            difficulty=DifficultyLevel.BEGINNER,
            progression_order=0,
            default_sets=3,
            default_reps=15,
            tips=[
                "Keep body straight from head to heels",
                "Hands slightly wider than shoulder-width",
                "Control the movement, don't bounce off the wall",
            ],
            common_mistakes=[
                "Letting hips sag or stick out",
                "Not going through full range of motion",
            ],
        ),
        Exercise(
            id="pushup_incline",
            name="Incline Push-ups",
            name_pl="Pompki od blatu",
            description="Hands on elevated surface (counter, bench, stairs), perform push-up motion.",
            muscle_groups=[MuscleGroup.CHEST, MuscleGroup.TRICEPS, MuscleGroup.SHOULDERS],
            difficulty=DifficultyLevel.BEGINNER_PLUS,
            progression_order=1,
            default_sets=3,
            default_reps=12,
            tips=[
                "Lower the surface height as you get stronger",
                "Start with counter height, progress to bench, then stairs",
                "Keep core tight throughout",
            ],
            common_mistakes=[
                "Surface too high (too easy) or too low (too hard)",
                "Flaring elbows out to 90 degrees",
            ],
        ),
        Exercise(
            id="pushup_knee",
            name="Knee Push-ups",
            name_pl="Pompki na kolanach",
            description="Push-ups with knees on the ground instead of toes.",
            muscle_groups=[MuscleGroup.CHEST, MuscleGroup.TRICEPS, MuscleGroup.SHOULDERS],
            difficulty=DifficultyLevel.EASY,
            progression_order=2,
            default_sets=3,
            default_reps=12,
            tips=[
                "Keep body straight from knees to head",
                "Don't let hips drop or pike up",
                "Place a mat under knees for comfort",
            ],
            common_mistakes=[
                "Hips too high (piking)",
                "Not lowering chest close enough to ground",
            ],
        ),
        Exercise(
            id="pushup_full",
            name="Full Push-ups",
            name_pl="Pełne pompki",
            description="Standard push-up from toes with full body straight.",
            muscle_groups=[MuscleGroup.CHEST, MuscleGroup.TRICEPS, MuscleGroup.SHOULDERS, MuscleGroup.CORE],
            difficulty=DifficultyLevel.INTERMEDIATE,
            progression_order=3,
            default_sets=3,
            default_reps=10,
            tips=[
                "Arms at 45-degree angle from body",
                "Lower until chest nearly touches ground",
                "Squeeze glutes and brace core",
            ],
            common_mistakes=[
                "Sagging hips",
                "Incomplete range of motion",
                "Holding breath",
            ],
        ),
        Exercise(
            id="pushup_diamond",
            name="Diamond Push-ups",
            name_pl="Pompki diamentowe",
            description="Push-up with hands close together forming a diamond shape.",
            muscle_groups=[MuscleGroup.TRICEPS, MuscleGroup.CHEST, MuscleGroup.SHOULDERS],
            difficulty=DifficultyLevel.INTERMEDIATE_PLUS,
            progression_order=4,
            default_sets=3,
            default_reps=8,
            tips=[
                "Index fingers and thumbs touch to form diamond",
                "Keep elbows close to body",
                "Excellent tricep builder",
            ],
            common_mistakes=[
                "Hands too far apart (defeats purpose)",
                "Flaring elbows out",
            ],
        ),
        Exercise(
            id="pushup_archer",
            name="Archer Push-ups",
            name_pl="Pompki łucznika",
            description="Wide push-up where you shift weight to one arm while the other stays straight.",
            muscle_groups=[MuscleGroup.CHEST, MuscleGroup.TRICEPS, MuscleGroup.SHOULDERS, MuscleGroup.CORE],
            difficulty=DifficultyLevel.ADVANCED,
            progression_order=5,
            default_sets=3,
            default_reps=6,
            tips=[
                "Alternate sides each rep",
                "Keep straight arm locked",
                "Great preparation for one-arm push-ups",
            ],
            common_mistakes=[
                "Bending the extended arm",
                "Rotating torso too much",
            ],
        ),
        Exercise(
            id="pushup_onearm",
            name="One-arm Push-ups",
            name_pl="Pompki na jednej ręce",
            description="Push-up performed with only one arm while other is behind back.",
            muscle_groups=[MuscleGroup.CHEST, MuscleGroup.TRICEPS, MuscleGroup.SHOULDERS, MuscleGroup.CORE],
            difficulty=DifficultyLevel.EXPERT,
            progression_order=6,
            default_sets=3,
            default_reps=5,
            tips=[
                "Wider foot stance for balance",
                "Keep hips square to ground",
                "Start with incline version if needed",
            ],
            common_mistakes=[
                "Rotating hips open",
                "Not going through full range of motion",
            ],
        ),
    ],
)


# =============================================================================
# SQUAT PROGRESSION
# Assisted → Box → Full → Bulgarian → Pistol
# =============================================================================

SQUAT_PROGRESSION = ProgressionChain(
    id="squat",
    name="Squat Progression",
    name_pl="Progresja Przysiadów",
    description="Progress from assisted squats to pistol squats",
    exercises=[
        Exercise(
            id="squat_assisted",
            name="Assisted Squats",
            name_pl="Przysiady z asekuracją",
            description="Hold onto a sturdy object for balance while squatting.",
            muscle_groups=[MuscleGroup.QUADRICEPS, MuscleGroup.GLUTES, MuscleGroup.HAMSTRINGS],
            difficulty=DifficultyLevel.BEGINNER,
            progression_order=0,
            default_sets=3,
            default_reps=15,
            tips=[
                "Use a doorframe, pole, or TRX straps",
                "Focus on proper squat form",
                "Gradually reduce assistance",
            ],
            common_mistakes=[
                "Relying too much on arm support",
                "Knees caving inward",
            ],
        ),
        Exercise(
            id="squat_box",
            name="Box Squats",
            name_pl="Przysiady na skrzynię",
            description="Squat down to a box or chair, pause, then stand.",
            muscle_groups=[MuscleGroup.QUADRICEPS, MuscleGroup.GLUTES, MuscleGroup.HAMSTRINGS],
            difficulty=DifficultyLevel.BEGINNER_PLUS,
            progression_order=1,
            default_sets=3,
            default_reps=12,
            tips=[
                "Touch the box but don't sit fully",
                "Lower box height as you progress",
                "Pause briefly at bottom",
            ],
            common_mistakes=[
                "Plopping onto the box",
                "Using momentum to stand up",
            ],
        ),
        Exercise(
            id="squat_full",
            name="Full Squats",
            name_pl="Pełne przysiady",
            description="Bodyweight squat with full depth (thighs parallel or below).",
            muscle_groups=[MuscleGroup.QUADRICEPS, MuscleGroup.GLUTES, MuscleGroup.HAMSTRINGS, MuscleGroup.CORE],
            difficulty=DifficultyLevel.EASY,
            progression_order=2,
            default_sets=3,
            default_reps=15,
            tips=[
                "Feet shoulder-width apart, toes slightly out",
                "Keep chest up and back straight",
                "Drive through heels to stand",
            ],
            common_mistakes=[
                "Heels coming off ground",
                "Knees caving inward",
                "Rounding lower back",
            ],
        ),
        Exercise(
            id="squat_close",
            name="Close Squats",
            name_pl="Przysiady wąskie",
            description="Squat with feet close together.",
            muscle_groups=[MuscleGroup.QUADRICEPS, MuscleGroup.GLUTES, MuscleGroup.HAMSTRINGS],
            difficulty=DifficultyLevel.INTERMEDIATE,
            progression_order=3,
            default_sets=3,
            default_reps=12,
            tips=[
                "Feet touching or very close together",
                "Arms forward for balance",
                "Work on ankle mobility",
            ],
            common_mistakes=[
                "Heels lifting off ground",
                "Falling backwards",
            ],
        ),
        Exercise(
            id="squat_bulgarian",
            name="Bulgarian Split Squats",
            name_pl="Bułgarskie przysiady",
            description="Single leg squat with rear foot elevated on bench.",
            muscle_groups=[MuscleGroup.QUADRICEPS, MuscleGroup.GLUTES, MuscleGroup.HAMSTRINGS],
            difficulty=DifficultyLevel.INTERMEDIATE_PLUS,
            progression_order=4,
            default_sets=3,
            default_reps=8,
            tips=[
                "Rear foot laces down on bench",
                "Front foot far enough forward",
                "Keep torso upright",
            ],
            common_mistakes=[
                "Leaning too far forward",
                "Front knee going past toes excessively",
            ],
        ),
        Exercise(
            id="squat_shrimp",
            name="Shrimp Squats",
            name_pl="Przysiady krewetka",
            description="Single leg squat holding rear foot behind you.",
            muscle_groups=[MuscleGroup.QUADRICEPS, MuscleGroup.GLUTES, MuscleGroup.HAMSTRINGS, MuscleGroup.CORE],
            difficulty=DifficultyLevel.ADVANCED,
            progression_order=5,
            default_sets=3,
            default_reps=5,
            tips=[
                "Hold rear foot with hand behind back",
                "Touch rear knee to ground",
                "Keep torso upright",
            ],
            common_mistakes=[
                "Falling to the side",
                "Not touching knee to ground",
            ],
        ),
        Exercise(
            id="squat_pistol",
            name="Pistol Squats",
            name_pl="Przysiady pistoletowe",
            description="Single leg squat with other leg extended straight in front.",
            muscle_groups=[MuscleGroup.QUADRICEPS, MuscleGroup.GLUTES, MuscleGroup.HAMSTRINGS, MuscleGroup.CORE],
            difficulty=DifficultyLevel.EXPERT,
            progression_order=6,
            default_sets=3,
            default_reps=5,
            tips=[
                "Extend non-working leg straight ahead",
                "Arms forward for counterbalance",
                "Go as deep as mobility allows",
            ],
            common_mistakes=[
                "Falling backwards",
                "Not reaching full depth",
                "Bending extended leg",
            ],
        ),
    ],
)


# =============================================================================
# PULL-UP PROGRESSION
# Dead Hang → Scapular Pulls → Negatives → Assisted → Full → Weighted
# =============================================================================

PULL_UP_PROGRESSION = ProgressionChain(
    id="pullup",
    name="Pull-up Progression",
    name_pl="Progresja Podciągnięć",
    description="Progress from dead hangs to weighted pull-ups",
    exercises=[
        Exercise(
            id="pullup_deadhang",
            name="Dead Hang",
            name_pl="Martwy zwis",
            description="Hang from bar with straight arms to build grip strength.",
            muscle_groups=[MuscleGroup.BACK, MuscleGroup.BICEPS],
            difficulty=DifficultyLevel.BEGINNER,
            progression_order=0,
            default_sets=3,
            default_reps=1,
            default_hold_seconds=30,
            tips=[
                "Grip bar slightly wider than shoulder-width",
                "Let shoulders shrug up naturally",
                "Build up to 60 second holds",
            ],
            common_mistakes=[
                "Gripping too narrow or wide",
                "Not fully extending arms",
            ],
        ),
        Exercise(
            id="pullup_scapular",
            name="Scapular Pull-ups",
            name_pl="Podciągnięcia łopatkowe",
            description="From dead hang, retract shoulder blades without bending arms.",
            muscle_groups=[MuscleGroup.BACK],
            difficulty=DifficultyLevel.BEGINNER_PLUS,
            progression_order=1,
            default_sets=3,
            default_reps=10,
            tips=[
                "Keep arms straight throughout",
                "Focus on squeezing shoulder blades down and back",
                "Small movement but important activation",
            ],
            common_mistakes=[
                "Bending the arms",
                "Using momentum",
            ],
        ),
        Exercise(
            id="pullup_negative",
            name="Negative Pull-ups",
            name_pl="Negatywy podciągnięć",
            description="Jump to top position, lower yourself as slowly as possible.",
            muscle_groups=[MuscleGroup.BACK, MuscleGroup.BICEPS],
            difficulty=DifficultyLevel.EASY,
            progression_order=2,
            default_sets=3,
            default_reps=5,
            tips=[
                "Use a box to jump to top position",
                "Aim for 5-10 second descent",
                "Control the entire movement",
            ],
            common_mistakes=[
                "Dropping too fast",
                "Not starting from full top position",
            ],
        ),
        Exercise(
            id="pullup_assisted",
            name="Assisted Pull-ups",
            name_pl="Podciągnięcia z asystą",
            description="Pull-ups with band assistance or partner help.",
            muscle_groups=[MuscleGroup.BACK, MuscleGroup.BICEPS],
            difficulty=DifficultyLevel.EASY_PLUS,
            progression_order=3,
            default_sets=3,
            default_reps=8,
            tips=[
                "Use thinner bands as you get stronger",
                "Maintain proper form despite assistance",
                "Full range of motion every rep",
            ],
            common_mistakes=[
                "Using too much assistance",
                "Kipping or swinging",
            ],
        ),
        Exercise(
            id="pullup_full",
            name="Pull-ups",
            name_pl="Podciągnięcia",
            description="Full pull-up from dead hang to chin over bar.",
            muscle_groups=[MuscleGroup.BACK, MuscleGroup.BICEPS],
            difficulty=DifficultyLevel.INTERMEDIATE,
            progression_order=4,
            default_sets=3,
            default_reps=8,
            tips=[
                "Start from dead hang, chin over bar at top",
                "Initiate with scapular retraction",
                "Control the descent",
            ],
            common_mistakes=[
                "Kipping or using momentum",
                "Not going through full range of motion",
                "Chin not clearing the bar",
            ],
        ),
        Exercise(
            id="pullup_lsit",
            name="L-sit Pull-ups",
            name_pl="Podciągnięcia z L-sit",
            description="Pull-ups while holding legs extended in L-sit position.",
            muscle_groups=[MuscleGroup.BACK, MuscleGroup.BICEPS, MuscleGroup.CORE],
            difficulty=DifficultyLevel.ADVANCED,
            progression_order=5,
            default_sets=3,
            default_reps=5,
            tips=[
                "Keep legs parallel to ground",
                "Maintain core tension throughout",
                "Can bend knees slightly to start",
            ],
            common_mistakes=[
                "Legs dropping during pull",
                "Swinging for momentum",
            ],
        ),
        Exercise(
            id="pullup_archer",
            name="Archer Pull-ups",
            name_pl="Podciągnięcia łucznika",
            description="Wide grip pull-up alternating to each side.",
            muscle_groups=[MuscleGroup.BACK, MuscleGroup.BICEPS],
            difficulty=DifficultyLevel.ADVANCED_PLUS,
            progression_order=6,
            default_sets=3,
            default_reps=4,
            tips=[
                "Wide grip, pull to alternating sides",
                "Keep one arm straight as you pull",
                "Great progression toward one-arm pull-ups",
            ],
            common_mistakes=[
                "Not extending the non-working arm fully",
                "Using momentum",
            ],
        ),
    ],
)


# =============================================================================
# CORE PROGRESSION
# Plank → Side Plank → Leg Raises → L-sit → Dragon Flag
# =============================================================================

CORE_PROGRESSION = ProgressionChain(
    id="core",
    name="Core Progression",
    name_pl="Progresja Core",
    description="Progress from planks to advanced core exercises",
    exercises=[
        Exercise(
            id="core_plank",
            name="Plank",
            name_pl="Deska (plank)",
            description="Hold push-up position with arms straight or on forearms.",
            muscle_groups=[MuscleGroup.CORE],
            difficulty=DifficultyLevel.BEGINNER,
            progression_order=0,
            default_sets=3,
            default_reps=1,
            default_hold_seconds=30,
            tips=[
                "Body straight from head to heels",
                "Squeeze glutes and brace abs",
                "Don't let hips sag or pike",
            ],
            common_mistakes=[
                "Hips sagging down",
                "Hips piking up",
                "Holding breath",
            ],
        ),
        Exercise(
            id="core_side_plank",
            name="Side Plank",
            name_pl="Deska boczna",
            description="Hold body sideways supported on one forearm.",
            muscle_groups=[MuscleGroup.CORE],
            difficulty=DifficultyLevel.BEGINNER_PLUS,
            progression_order=1,
            default_sets=3,
            default_reps=1,
            default_hold_seconds=30,
            tips=[
                "Stack feet or stagger for easier version",
                "Keep hips up and body straight",
                "Equal time on both sides",
            ],
            common_mistakes=[
                "Hips dropping",
                "Leaning forward or backward",
            ],
        ),
        Exercise(
            id="core_knee_raise",
            name="Hanging Knee Raises",
            name_pl="Unoszenie kolan w zwisie",
            description="Hang from bar and raise knees toward chest.",
            muscle_groups=[MuscleGroup.CORE],
            difficulty=DifficultyLevel.EASY,
            progression_order=2,
            default_sets=3,
            default_reps=10,
            tips=[
                "Control the movement, no swinging",
                "Curl pelvis up at top",
                "Lower with control",
            ],
            common_mistakes=[
                "Using momentum to swing legs",
                "Not curling pelvis",
            ],
        ),
        Exercise(
            id="core_leg_raise",
            name="Hanging Leg Raises",
            name_pl="Unoszenie prostych nóg w zwisie",
            description="Hang from bar and raise straight legs to horizontal.",
            muscle_groups=[MuscleGroup.CORE],
            difficulty=DifficultyLevel.INTERMEDIATE,
            progression_order=3,
            default_sets=3,
            default_reps=8,
            tips=[
                "Keep legs straight throughout",
                "Raise until legs are parallel to ground",
                "Control the descent",
            ],
            common_mistakes=[
                "Bending knees",
                "Swinging for momentum",
            ],
        ),
        Exercise(
            id="core_toes_to_bar",
            name="Toes to Bar",
            name_pl="Palce do drążka",
            description="Hang from bar and raise straight legs to touch the bar.",
            muscle_groups=[MuscleGroup.CORE],
            difficulty=DifficultyLevel.INTERMEDIATE_PLUS,
            progression_order=4,
            default_sets=3,
            default_reps=6,
            tips=[
                "Touch toes to bar between hands",
                "Keep legs straight",
                "Controlled movement",
            ],
            common_mistakes=[
                "Kipping excessively",
                "Bending knees too much",
            ],
        ),
        Exercise(
            id="core_lsit",
            name="L-sit",
            name_pl="L-sit",
            description="Support body on parallel bars or floor with legs extended straight.",
            muscle_groups=[MuscleGroup.CORE, MuscleGroup.TRICEPS],
            difficulty=DifficultyLevel.ADVANCED,
            progression_order=5,
            default_sets=3,
            default_reps=1,
            default_hold_seconds=15,
            tips=[
                "Start on parallettes or dip bars",
                "Keep legs straight and parallel to ground",
                "Push shoulders down",
            ],
            common_mistakes=[
                "Bending knees",
                "Letting legs drop below parallel",
            ],
        ),
        Exercise(
            id="core_dragon_flag",
            name="Dragon Flag",
            name_pl="Flaga smoka",
            description="Lie on bench, grip behind head, raise body to vertical and lower with control.",
            muscle_groups=[MuscleGroup.CORE],
            difficulty=DifficultyLevel.EXPERT,
            progression_order=6,
            default_sets=3,
            default_reps=5,
            tips=[
                "Body straight from shoulders to toes",
                "Only shoulders touch the bench",
                "Control the descent - don't crash down",
            ],
            common_mistakes=[
                "Bending at hips",
                "Using momentum",
                "Lowering too fast",
            ],
        ),
    ],
)


# =============================================================================
# DIP PROGRESSION
# Bench Dips → Straight Bar → Parallel Bar → Ring Dips → Weighted
# =============================================================================

DIP_PROGRESSION = ProgressionChain(
    id="dip",
    name="Dip Progression",
    name_pl="Progresja Dipów",
    description="Progress from bench dips to weighted ring dips",
    exercises=[
        Exercise(
            id="dip_bench",
            name="Bench Dips",
            name_pl="Dipy na ławce",
            description="Hands on bench behind you, lower body by bending arms.",
            muscle_groups=[MuscleGroup.TRICEPS, MuscleGroup.CHEST, MuscleGroup.SHOULDERS],
            difficulty=DifficultyLevel.BEGINNER,
            progression_order=0,
            default_sets=3,
            default_reps=12,
            tips=[
                "Legs bent for easier, straight for harder",
                "Keep back close to bench",
                "Lower until upper arms parallel to ground",
            ],
            common_mistakes=[
                "Going too low (shoulder strain)",
                "Letting shoulders roll forward",
            ],
        ),
        Exercise(
            id="dip_negative",
            name="Negative Dips",
            name_pl="Negatywy dipów",
            description="Jump to top of dip position, lower yourself slowly.",
            muscle_groups=[MuscleGroup.TRICEPS, MuscleGroup.CHEST, MuscleGroup.SHOULDERS],
            difficulty=DifficultyLevel.EASY,
            progression_order=1,
            default_sets=3,
            default_reps=5,
            tips=[
                "Use a box to jump to top position",
                "Lower for 5-10 seconds",
                "Control the entire movement",
            ],
            common_mistakes=[
                "Lowering too fast",
                "Not starting from full lockout",
            ],
        ),
        Exercise(
            id="dip_assisted",
            name="Assisted Dips",
            name_pl="Dipy z asystą",
            description="Dips with band assistance or feet on ground for support.",
            muscle_groups=[MuscleGroup.TRICEPS, MuscleGroup.CHEST, MuscleGroup.SHOULDERS],
            difficulty=DifficultyLevel.EASY_PLUS,
            progression_order=2,
            default_sets=3,
            default_reps=8,
            tips=[
                "Loop band under knees",
                "Use thinner bands as you progress",
                "Maintain proper dip form",
            ],
            common_mistakes=[
                "Relying too much on band",
                "Swinging or bouncing",
            ],
        ),
        Exercise(
            id="dip_parallel",
            name="Parallel Bar Dips",
            name_pl="Dipy na poręczach",
            description="Full dips on parallel bars.",
            muscle_groups=[MuscleGroup.TRICEPS, MuscleGroup.CHEST, MuscleGroup.SHOULDERS],
            difficulty=DifficultyLevel.INTERMEDIATE,
            progression_order=3,
            default_sets=3,
            default_reps=8,
            tips=[
                "Lean forward slightly for chest emphasis",
                "Stay upright for tricep emphasis",
                "Lower until upper arms parallel to ground",
            ],
            common_mistakes=[
                "Going too low (shoulder strain)",
                "Swinging legs",
            ],
        ),
        Exercise(
            id="dip_ring",
            name="Ring Dips",
            name_pl="Dipy na kółkach",
            description="Dips on gymnastics rings for added instability.",
            muscle_groups=[MuscleGroup.TRICEPS, MuscleGroup.CHEST, MuscleGroup.SHOULDERS, MuscleGroup.CORE],
            difficulty=DifficultyLevel.ADVANCED,
            progression_order=4,
            default_sets=3,
            default_reps=6,
            tips=[
                "Turn rings out at top (RTO)",
                "Keep rings close to body",
                "Control the movement - rings are unstable",
            ],
            common_mistakes=[
                "Rings swinging or flaring out",
                "Not turning rings out at top",
            ],
        ),
        Exercise(
            id="dip_weighted",
            name="Weighted Dips",
            name_pl="Dipy z obciążeniem",
            description="Dips with added weight (belt, vest, or dumbbell between legs).",
            muscle_groups=[MuscleGroup.TRICEPS, MuscleGroup.CHEST, MuscleGroup.SHOULDERS],
            difficulty=DifficultyLevel.ADVANCED_PLUS,
            progression_order=5,
            default_sets=3,
            default_reps=5,
            tips=[
                "Start with small weights, progress gradually",
                "Use a dip belt for best loading",
                "Maintain perfect form despite weight",
            ],
            common_mistakes=[
                "Adding too much weight too fast",
                "Compromising form for more weight",
            ],
        ),
    ],
)


# =============================================================================
# ROW PROGRESSION
# Incline Rows → Horizontal Rows → Wide Rows → Archer → One-arm
# =============================================================================

ROW_PROGRESSION = ProgressionChain(
    id="row",
    name="Row Progression",
    name_pl="Progresja Wiosłowania",
    description="Progress from incline rows to one-arm rows",
    exercises=[
        Exercise(
            id="row_incline",
            name="Incline Rows",
            name_pl="Wiosłowanie pod kątem",
            description="Rows on bar set at high position (body more upright).",
            muscle_groups=[MuscleGroup.BACK, MuscleGroup.BICEPS],
            difficulty=DifficultyLevel.BEGINNER,
            progression_order=0,
            default_sets=3,
            default_reps=15,
            tips=[
                "Body straight from head to heels",
                "Pull chest to bar",
                "Lower bar height as you progress",
            ],
            common_mistakes=[
                "Sagging hips",
                "Not pulling chest all the way to bar",
            ],
        ),
        Exercise(
            id="row_horizontal",
            name="Horizontal Rows",
            name_pl="Wiosłowanie poziome",
            description="Body horizontal under bar, pull chest to bar.",
            muscle_groups=[MuscleGroup.BACK, MuscleGroup.BICEPS, MuscleGroup.CORE],
            difficulty=DifficultyLevel.EASY,
            progression_order=1,
            default_sets=3,
            default_reps=12,
            tips=[
                "Body parallel to ground",
                "Squeeze shoulder blades at top",
                "Keep core tight",
            ],
            common_mistakes=[
                "Hips sagging",
                "Not achieving full range of motion",
            ],
        ),
        Exercise(
            id="row_wide",
            name="Wide Rows",
            name_pl="Wiosłowanie szerokim chwytem",
            description="Horizontal rows with wide grip for more back emphasis.",
            muscle_groups=[MuscleGroup.BACK, MuscleGroup.BICEPS],
            difficulty=DifficultyLevel.EASY_PLUS,
            progression_order=2,
            default_sets=3,
            default_reps=10,
            tips=[
                "Grip 1.5x shoulder width",
                "Pull to lower chest",
                "Focus on squeezing back muscles",
            ],
            common_mistakes=[
                "Grip too narrow",
                "Using arms instead of back",
            ],
        ),
        Exercise(
            id="row_feet_elevated",
            name="Feet Elevated Rows",
            name_pl="Wiosłowanie z nogami na podwyższeniu",
            description="Horizontal rows with feet elevated for increased difficulty.",
            muscle_groups=[MuscleGroup.BACK, MuscleGroup.BICEPS, MuscleGroup.CORE],
            difficulty=DifficultyLevel.INTERMEDIATE,
            progression_order=3,
            default_sets=3,
            default_reps=10,
            tips=[
                "Elevate feet on box or bench",
                "Maintain straight body line",
                "Full range of motion",
            ],
            common_mistakes=[
                "Hips dropping",
                "Incomplete pull",
            ],
        ),
        Exercise(
            id="row_archer",
            name="Archer Rows",
            name_pl="Wiosłowanie łucznika",
            description="Wide row pulling to one side while other arm stays straight.",
            muscle_groups=[MuscleGroup.BACK, MuscleGroup.BICEPS],
            difficulty=DifficultyLevel.INTERMEDIATE_PLUS,
            progression_order=4,
            default_sets=3,
            default_reps=6,
            tips=[
                "Alternate sides",
                "Keep non-working arm straight",
                "Full range of motion to working side",
            ],
            common_mistakes=[
                "Bending the extended arm",
                "Rotating torso excessively",
            ],
        ),
        Exercise(
            id="row_onearm",
            name="One-arm Rows",
            name_pl="Wiosłowanie na jednej ręce",
            description="Horizontal row using only one arm.",
            muscle_groups=[MuscleGroup.BACK, MuscleGroup.BICEPS, MuscleGroup.CORE],
            difficulty=DifficultyLevel.ADVANCED,
            progression_order=5,
            default_sets=3,
            default_reps=5,
            tips=[
                "Wider foot stance for stability",
                "Keep hips square to ground",
                "Start at higher incline if needed",
            ],
            common_mistakes=[
                "Rotating hips open",
                "Using momentum",
            ],
        ),
    ],
)


# =============================================================================
# ALL PROGRESSIONS
# =============================================================================

ALL_PROGRESSIONS = [
    PUSH_UP_PROGRESSION,
    SQUAT_PROGRESSION,
    PULL_UP_PROGRESSION,
    CORE_PROGRESSION,
    DIP_PROGRESSION,
    ROW_PROGRESSION,
]


def get_all_exercises() -> list[Exercise]:
    """Get all exercises from all progression chains."""
    exercises = []
    for chain in ALL_PROGRESSIONS:
        exercises.extend(chain.exercises)
    return exercises
