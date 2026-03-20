import struct
import sys
import os

BRACKET_FILE = "all_valid_brackets.bin"

# ------------------------------------------------------------
# REGION ORDER (must match the generator)
#
# 0 = Fort Worth 1   (UConn region)
# 1 = Sacramento 4   (South Carolina region)
# 2 = Sacramento 2   (UCLA region)
# 3 = Fort Worth 3   (Texas region)
# ------------------------------------------------------------

REGIONS = [
    {
        "name": "Fort Worth 1",
        "teams": [
            "1 UConn",
            "16 Iona",
            "8 Iowa St.",
            "9 Syracuse",
            "5 Maryland",
            "12 Murray St.",
            "4 North Carolina",
            "13 Western Illinois",
            "6 Notre Dame",
            "11 Fairfield",
            "3 Ohio St.",
            "14 Howard",
            "7 Illinois",
            "10 Colorado",
            "2 Vanderbilt",
            "15 High Point",
        ]
    },
    {
        "name": "Sacramento 4",
        "teams": [
            "1 South Carolina",
            "16 Southern U.",
            "8 Clemson",
            "9 Southern California",
            "5 Michigan St.",
            "12 Colorado St.",
            "4 Oklahoma",
            "13 Idaho",
            "6 Washington",
            "11 South Dakota St.",
            "3 TCU",
            "14 UC San Diego",
            "7 Georgia",
            "10 Virginia",
            "2 Iowa",
            "15 FDU",
        ]
    },
    {
        "name": "Sacramento 2",
        "teams": [
            "1 UCLA",
            "16 Oklahoma St.",
            "8 Princeton",
            "9 Ole Miss",
            "5 Gonzaga",
            "12 Minnesota",
            "4 Green Bay",
            "13 Baylor",
            "6 Nebraska",
            "11 Duke",
            "3 Col. of Charleston",
            "14 Texas Tech",
            "7 Villanova",
            "10 LSU",
            "2 USC",
            "15 Jacksonville",
        ]
    },
    {
        "name": "Fort Worth 3",
        "teams": [
            "1 Texas",
            "16 Missouri St.",
            "8 Oregon",
            "9 Virginia Tech",
            "5 Kentucky",
            "12 James Madison",
            "4 West Virginia",
            "13 Miami (OH)",
            "6 Alabama",
            "11 Rhode Island",
            "3 Louisville",
            "14 Vermont",
            "7 NC State",
            "10 Tennessee",
            "2 Michigan",
            "15 Holy Cross",
        ]
    },
]

# ------------------------------------------------------------
# GAME BIT HELPERS
# ------------------------------------------------------------

def get_bit(mask: int, bit_index: int) -> int:
    return (mask >> bit_index) & 1


def region_round1_game_bit(region_index, local_game_index):
    return region_index * 8 + local_game_index


def region_round2_game_bit(region_index, local_game_index):
    return 32 + region_index * 4 + local_game_index


def region_sweet16_game_bit(region_index, local_game_index):
    return 48 + region_index * 2 + local_game_index


def region_elite8_game_bit(region_index):
    return 56 + region_index


def final_four_bit(local_game_index):
    return 60 + local_game_index


TITLE_GAME_BIT = 62


# ------------------------------------------------------------
# BRACKET STRUCTURE
# ------------------------------------------------------------

def get_round1_matchups_for_region(region_index):
    teams = REGIONS[region_index]["teams"]

    # team positions:
    # 0  = 1-seed
    # 1  = 16-seed
    # 2  = 8-seed
    # 3  = 9-seed
    # 4  = 5-seed
    # 5  = 12-seed
    # 6  = 4-seed
    # 7  = 13-seed
    # 8  = 6-seed
    # 9  = 11-seed
    # 10 = 3-seed
    # 11 = 14-seed
    # 12 = 7-seed
    # 13 = 10-seed
    # 14 = 2-seed
    # 15 = 15-seed

    return [
        (teams[0], teams[1]),   # 1 vs 16
        (teams[2], teams[3]),   # 8 vs 9
        (teams[4], teams[5]),   # 5 vs 12
        (teams[6], teams[7]),   # 4 vs 13
        (teams[8], teams[9]),   # 6 vs 11
        (teams[10], teams[11]), # 3 vs 14
        (teams[12], teams[13]), # 7 vs 10
        (teams[14], teams[15]), # 2 vs 15
    ]


def choose_winner(top_team, bottom_team, bit_value):
    if bit_value == 0:
        return top_team
    else:
        return bottom_team


def decode_region(region_index, mask):
    region_name = REGIONS[region_index]["name"]

    # -------------------------
    # Round 1
    # -------------------------
    round1_matchups = get_round1_matchups_for_region(region_index)
    round1_winners = []

    for local_game_index, (top_team, bottom_team) in enumerate(round1_matchups):
        bit = region_round1_game_bit(region_index, local_game_index)
        winner = choose_winner(top_team, bottom_team, get_bit(mask, bit))
        round1_winners.append(winner)

    # -------------------------
    # Round 2
    # -------------------------
    round2_matchups = [
        (round1_winners[0], round1_winners[1]),
        (round1_winners[2], round1_winners[3]),
        (round1_winners[4], round1_winners[5]),
        (round1_winners[6], round1_winners[7]),
    ]

    round2_winners = []
    for local_game_index, (top_team, bottom_team) in enumerate(round2_matchups):
        bit = region_round2_game_bit(region_index, local_game_index)
        winner = choose_winner(top_team, bottom_team, get_bit(mask, bit))
        round2_winners.append(winner)

    # -------------------------
    # Sweet 16
    # -------------------------
    sweet16_matchups = [
        (round2_winners[0], round2_winners[1]),
        (round2_winners[2], round2_winners[3]),
    ]

    sweet16_winners = []
    for local_game_index, (top_team, bottom_team) in enumerate(sweet16_matchups):
        bit = region_sweet16_game_bit(region_index, local_game_index)
        winner = choose_winner(top_team, bottom_team, get_bit(mask, bit))
        sweet16_winners.append(winner)

    # -------------------------
    # Elite 8
    # -------------------------
    elite8_matchup = (sweet16_winners[0], sweet16_winners[1])
    elite8_bit = region_elite8_game_bit(region_index)
    region_champ = choose_winner(elite8_matchup[0], elite8_matchup[1], get_bit(mask, elite8_bit))

    return {
        "region_name": region_name,
        "round1_matchups": round1_matchups,
        "round1_winners": round1_winners,
        "round2_matchups": round2_matchups,
        "round2_winners": round2_winners,
        "sweet16_matchups": sweet16_matchups,
        "sweet16_winners": sweet16_winners,
        "elite8_matchup": elite8_matchup,
        "region_champ": region_champ,
    }


def decode_full_bracket(mask):
    regions = [decode_region(i, mask) for i in range(4)]

    # Final Four pairings must match the generator:
    # semifinal 1: region 0 vs region 1
    # semifinal 2: region 2 vs region 3
    ff1_top = regions[0]["region_champ"]
    ff1_bottom = regions[1]["region_champ"]
    ff2_top = regions[2]["region_champ"]
    ff2_bottom = regions[3]["region_champ"]

    ff1_winner = choose_winner(ff1_top, ff1_bottom, get_bit(mask, final_four_bit(0)))
    ff2_winner = choose_winner(ff2_top, ff2_bottom, get_bit(mask, final_four_bit(1)))
    champion = choose_winner(ff1_winner, ff2_winner, get_bit(mask, TITLE_GAME_BIT))

    return {
        "regions": regions,
        "final_four_matchups": [
            (ff1_top, ff1_bottom),
            (ff2_top, ff2_bottom),
        ],
        "final_four_winners": [
            ff1_winner,
            ff2_winner,
        ],
        "championship_matchup": (ff1_winner, ff2_winner),
        "champion": champion,
    }


def read_bracket_mask(filename, bracket_index):
    file_size = os.path.getsize(filename)
    total_brackets = file_size // 8

    if bracket_index < 0 or bracket_index >= total_brackets:
        raise ValueError(f"Bracket index must be between 0 and {total_brackets - 1}")

    with open(filename, "rb") as f:
        f.seek(bracket_index * 8)
        data = f.read(8)
        if len(data) != 8:
            raise ValueError("Could not read 8 bytes for bracket")
        return struct.unpack("<Q", data)[0], total_brackets


def print_region(region):
    print(f"\n==============================")
    print(f"{region['region_name']}")
    print(f"==============================")

    print("\nRound 1:")
    for i, ((top, bottom), winner) in enumerate(zip(region["round1_matchups"], region["round1_winners"]), start=1):
        print(f"  Game {i}: {top} vs {bottom} -> {winner}")

    print("\nRound 2:")
    for i, ((top, bottom), winner) in enumerate(zip(region["round2_matchups"], region["round2_winners"]), start=1):
        print(f"  Game {i}: {top} vs {bottom} -> {winner}")

    print("\nSweet 16:")
    for i, ((top, bottom), winner) in enumerate(zip(region["sweet16_matchups"], region["sweet16_winners"]), start=1):
        print(f"  Game {i}: {top} vs {bottom} -> {winner}")

    print("\nElite 8:")
    top, bottom = region["elite8_matchup"]
    print(f"  {top} vs {bottom} -> {region['region_champ']}")


def print_full_bracket(decoded, bracket_index, total_brackets, mask):
    print(f"\n============================================================")
    print(f"BRACKET #{bracket_index:,} of {total_brackets:,}")
    print(f"64-bit mask value: {mask}")
    print(f"============================================================")

    for region in decoded["regions"]:
        print_region(region)

    print(f"\n==============================")
    print("FINAL FOUR")
    print(f"==============================")

    (ff1_top, ff1_bottom), (ff2_top, ff2_bottom) = decoded["final_four_matchups"]
    ff1_winner, ff2_winner = decoded["final_four_winners"]
    title_top, title_bottom = decoded["championship_matchup"]

    print(f"\nNational Semifinal 1:")
    print(f"  {ff1_top} vs {ff1_bottom} -> {ff1_winner}")

    print(f"\nNational Semifinal 2:")
    print(f"  {ff2_top} vs {ff2_bottom} -> {ff2_winner}")

    print(f"\nNational Championship:")
    print(f"  {title_top} vs {title_bottom} -> {decoded['champion']}")

    print(f"\nCHAMPION: {decoded['champion']}")


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("  python read_bracket.py 0")
        print("  python read_bracket.py 12345")
        return

    bracket_index = int(sys.argv[1])

    mask, total_brackets = read_bracket_mask(BRACKET_FILE, bracket_index)
    decoded = decode_full_bracket(mask)
    print_full_bracket(decoded, bracket_index, total_brackets, mask)


if __name__ == "__main__":
    main()