"""
Comprehensive NFL player database
Includes offensive and defensive players from all teams
"""
from typing import Dict, List

# Comprehensive NFL player database
NFL_PLAYERS: Dict[str, List[Dict]] = {
    # Kansas City Chiefs
    "Kansas City Chiefs": [
        # Offense
        {"name": "Patrick Mahomes", "position": "QB", "type": "offense", "stats": {"yards_per_game": 285, "touchdowns": 2.1}},
        {"name": "Travis Kelce", "position": "TE", "type": "offense", "stats": {"yards_per_game": 75, "touchdowns": 0.8}},
        {"name": "Rashee Rice", "position": "WR", "type": "offense", "stats": {"yards_per_game": 65, "touchdowns": 0.6}},
        {"name": "Isiah Pacheco", "position": "RB", "type": "offense", "stats": {"yards_per_game": 85, "touchdowns": 0.7}},
        {"name": "Marquez Valdes-Scantling", "position": "WR", "type": "offense", "stats": {"yards_per_game": 45, "touchdowns": 0.4}},
        # Defense
        {"name": "Chris Jones", "position": "DT", "type": "defense", "stats": {"tackles_per_game": 4.2, "sacks": 0.8}},
        {"name": "Nick Bolton", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 8.5, "sacks": 0.3}},
        {"name": "L'Jarius Sneed", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 5.1, "interceptions": 0.2}},
    ],
    
    # Buffalo Bills
    "Buffalo Bills": [
        # Offense
        {"name": "Josh Allen", "position": "QB", "type": "offense", "stats": {"yards_per_game": 275, "touchdowns": 2.3}},
        {"name": "Stefon Diggs", "position": "WR", "type": "offense", "stats": {"yards_per_game": 95, "touchdowns": 0.9}},
        {"name": "James Cook", "position": "RB", "type": "offense", "stats": {"yards_per_game": 90, "touchdowns": 0.6}},
        {"name": "Dalton Kincaid", "position": "TE", "type": "offense", "stats": {"yards_per_game": 55, "touchdowns": 0.5}},
        {"name": "Gabe Davis", "position": "WR", "type": "offense", "stats": {"yards_per_game": 50, "touchdowns": 0.5}},
        # Defense
        {"name": "Von Miller", "position": "OLB", "type": "defense", "stats": {"tackles_per_game": 3.8, "sacks": 0.6}},
        {"name": "Matt Milano", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 7.2, "sacks": 0.4}},
        {"name": "Tre'Davious White", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 4.5, "interceptions": 0.3}},
    ],
    
    # Philadelphia Eagles
    "Philadelphia Eagles": [
        # Offense
        {"name": "Jalen Hurts", "position": "QB", "type": "offense", "stats": {"yards_per_game": 260, "touchdowns": 2.0}},
        {"name": "A.J. Brown", "position": "WR", "type": "offense", "stats": {"yards_per_game": 100, "touchdowns": 0.9}},
        {"name": "DeVonta Smith", "position": "WR", "type": "offense", "stats": {"yards_per_game": 85, "touchdowns": 0.7}},
        {"name": "D'Andre Swift", "position": "RB", "type": "offense", "stats": {"yards_per_game": 75, "touchdowns": 0.6}},
        {"name": "Dallas Goedert", "position": "TE", "type": "offense", "stats": {"yards_per_game": 60, "touchdowns": 0.5}},
        # Defense
        {"name": "Haason Reddick", "position": "OLB", "type": "defense", "stats": {"tackles_per_game": 5.2, "sacks": 0.9}},
        {"name": "Fletcher Cox", "position": "DT", "type": "defense", "stats": {"tackles_per_game": 3.5, "sacks": 0.5}},
        {"name": "Darius Slay", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 4.8, "interceptions": 0.2}},
    ],
    
    # San Francisco 49ers
    "San Francisco 49ers": [
        # Offense
        {"name": "Brock Purdy", "position": "QB", "type": "offense", "stats": {"yards_per_game": 270, "touchdowns": 2.2}},
        {"name": "Christian McCaffrey", "position": "RB", "type": "offense", "stats": {"yards_per_game": 110, "touchdowns": 1.0}},
        {"name": "Deebo Samuel", "position": "WR", "type": "offense", "stats": {"yards_per_game": 70, "touchdowns": 0.6}},
        {"name": "Brandon Aiyuk", "position": "WR", "type": "offense", "stats": {"yards_per_game": 80, "touchdowns": 0.7}},
        {"name": "George Kittle", "position": "TE", "type": "offense", "stats": {"yards_per_game": 65, "touchdowns": 0.6}},
        # Defense
        {"name": "Nick Bosa", "position": "DE", "type": "defense", "stats": {"tackles_per_game": 4.8, "sacks": 1.1}},
        {"name": "Fred Warner", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 9.2, "sacks": 0.2}},
        {"name": "Charvarius Ward", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 5.5, "interceptions": 0.2}},
    ],
    
    # Baltimore Ravens
    "Baltimore Ravens": [
        # Offense
        {"name": "Lamar Jackson", "position": "QB", "type": "offense", "stats": {"yards_per_game": 240, "touchdowns": 1.8}},
        {"name": "Mark Andrews", "position": "TE", "type": "offense", "stats": {"yards_per_game": 70, "touchdowns": 0.7}},
        {"name": "Zay Flowers", "position": "WR", "type": "offense", "stats": {"yards_per_game": 60, "touchdowns": 0.5}},
        {"name": "Gus Edwards", "position": "RB", "type": "offense", "stats": {"yards_per_game": 65, "touchdowns": 0.6}},
        {"name": "Odell Beckham Jr.", "position": "WR", "type": "offense", "stats": {"yards_per_game": 45, "touchdowns": 0.4}},
        # Defense
        {"name": "Roquan Smith", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 10.1, "sacks": 0.3}},
        {"name": "Kyle Hamilton", "position": "S", "type": "defense", "stats": {"tackles_per_game": 6.8, "interceptions": 0.3}},
        {"name": "Justin Madubuike", "position": "DT", "type": "defense", "stats": {"tackles_per_game": 3.9, "sacks": 0.7}},
    ],
    
    # Miami Dolphins
    "Miami Dolphins": [
        # Offense
        {"name": "Tua Tagovailoa", "position": "QB", "type": "offense", "stats": {"yards_per_game": 290, "touchdowns": 2.4}},
        {"name": "Tyreek Hill", "position": "WR", "type": "offense", "stats": {"yards_per_game": 95, "touchdowns": 0.9}},
        {"name": "Jaylen Waddle", "position": "WR", "type": "offense", "stats": {"yards_per_game": 75, "touchdowns": 0.7}},
        {"name": "Raheem Mostert", "position": "RB", "type": "offense", "stats": {"yards_per_game": 80, "touchdowns": 0.8}},
        {"name": "Durham Smythe", "position": "TE", "type": "offense", "stats": {"yards_per_game": 25, "touchdowns": 0.2}},
        # Defense
        {"name": "Jaelan Phillips", "position": "OLB", "type": "defense", "stats": {"tackles_per_game": 4.5, "sacks": 0.8}},
        {"name": "Jevon Holland", "position": "S", "type": "defense", "stats": {"tackles_per_game": 6.2, "interceptions": 0.3}},
        {"name": "Xavien Howard", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 4.8, "interceptions": 0.2}},
    ],
    
    # Dallas Cowboys
    "Dallas Cowboys": [
        # Offense
        {"name": "Dak Prescott", "position": "QB", "type": "offense", "stats": {"yards_per_game": 280, "touchdowns": 2.2}},
        {"name": "CeeDee Lamb", "position": "WR", "type": "offense", "stats": {"yards_per_game": 105, "touchdowns": 1.0}},
        {"name": "Tony Pollard", "position": "RB", "type": "offense", "stats": {"yards_per_game": 85, "touchdowns": 0.7}},
        {"name": "Brandin Cooks", "position": "WR", "type": "offense", "stats": {"yards_per_game": 55, "touchdowns": 0.5}},
        {"name": "Jake Ferguson", "position": "TE", "type": "offense", "stats": {"yards_per_game": 50, "touchdowns": 0.5}},
        # Defense
        {"name": "Micah Parsons", "position": "OLB", "type": "defense", "stats": {"tackles_per_game": 5.8, "sacks": 1.0}},
        {"name": "Trevon Diggs", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 4.2, "interceptions": 0.4}},
        {"name": "DeMarcus Lawrence", "position": "DE", "type": "defense", "stats": {"tackles_per_game": 4.5, "sacks": 0.6}},
    ],
    
    # Detroit Lions
    "Detroit Lions": [
        # Offense
        {"name": "Jared Goff", "position": "QB", "type": "offense", "stats": {"yards_per_game": 265, "touchdowns": 2.0}},
        {"name": "Amon-Ra St. Brown", "position": "WR", "type": "offense", "stats": {"yards_per_game": 90, "touchdowns": 0.8}},
        {"name": "David Montgomery", "position": "RB", "type": "offense", "stats": {"yards_per_game": 75, "touchdowns": 0.7}},
        {"name": "Sam LaPorta", "position": "TE", "type": "offense", "stats": {"yards_per_game": 60, "touchdowns": 0.6}},
        {"name": "Jameson Williams", "position": "WR", "type": "offense", "stats": {"yards_per_game": 50, "touchdowns": 0.5}},
        # Defense
        {"name": "Aidan Hutchinson", "position": "DE", "type": "defense", "stats": {"tackles_per_game": 5.2, "sacks": 0.9}},
        {"name": "Alex Anzalone", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 7.8, "sacks": 0.3}},
        {"name": "Cameron Sutton", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 5.1, "interceptions": 0.2}},
    ],
    
    # Cincinnati Bengals
    "Cincinnati Bengals": [
        # Offense
        {"name": "Joe Burrow", "position": "QB", "type": "offense", "stats": {"yards_per_game": 275, "touchdowns": 2.1}},
        {"name": "Ja'Marr Chase", "position": "WR", "type": "offense", "stats": {"yards_per_game": 100, "touchdowns": 0.9}},
        {"name": "Tee Higgins", "position": "WR", "type": "offense", "stats": {"yards_per_game": 70, "touchdowns": 0.6}},
        {"name": "Joe Mixon", "position": "RB", "type": "offense", "stats": {"yards_per_game": 70, "touchdowns": 0.6}},
        {"name": "Irv Smith Jr.", "position": "TE", "type": "offense", "stats": {"yards_per_game": 35, "touchdowns": 0.3}},
        # Defense
        {"name": "Trey Hendrickson", "position": "DE", "type": "defense", "stats": {"tackles_per_game": 4.2, "sacks": 0.9}},
        {"name": "Logan Wilson", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 8.5, "sacks": 0.2}},
        {"name": "Chidobe Awuzie", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 5.0, "interceptions": 0.2}},
    ],
    
    # Green Bay Packers
    "Green Bay Packers": [
        # Offense
        {"name": "Jordan Love", "position": "QB", "type": "offense", "stats": {"yards_per_game": 250, "touchdowns": 2.0}},
        {"name": "Aaron Jones", "position": "RB", "type": "offense", "stats": {"yards_per_game": 75, "touchdowns": 0.6}},
        {"name": "Christian Watson", "position": "WR", "type": "offense", "stats": {"yards_per_game": 60, "touchdowns": 0.5}},
        {"name": "Romeo Doubs", "position": "WR", "type": "offense", "stats": {"yards_per_game": 55, "touchdowns": 0.5}},
        {"name": "Luke Musgrave", "position": "TE", "type": "offense", "stats": {"yards_per_game": 40, "touchdowns": 0.4}},
        # Defense
        {"name": "Rashan Gary", "position": "OLB", "type": "defense", "stats": {"tackles_per_game": 4.8, "sacks": 0.8}},
        {"name": "Kenny Clark", "position": "DT", "type": "defense", "stats": {"tackles_per_game": 4.0, "sacks": 0.5}},
        {"name": "Jaire Alexander", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 4.5, "interceptions": 0.3}},
    ],
    
    # Houston Texans
    "Houston Texans": [
        # Offense
        {"name": "C.J. Stroud", "position": "QB", "type": "offense", "stats": {"yards_per_game": 270, "touchdowns": 2.1}},
        {"name": "Nico Collins", "position": "WR", "type": "offense", "stats": {"yards_per_game": 85, "touchdowns": 0.7}},
        {"name": "Tank Dell", "position": "WR", "type": "offense", "stats": {"yards_per_game": 70, "touchdowns": 0.6}},
        {"name": "Dameon Pierce", "position": "RB", "type": "offense", "stats": {"yards_per_game": 65, "touchdowns": 0.5}},
        {"name": "Dalton Schultz", "position": "TE", "type": "offense", "stats": {"yards_per_game": 50, "touchdowns": 0.4}},
        # Defense
        {"name": "Will Anderson Jr.", "position": "DE", "type": "defense", "stats": {"tackles_per_game": 4.5, "sacks": 0.7}},
        {"name": "Jonathan Greenard", "position": "DE", "type": "defense", "stats": {"tackles_per_game": 4.2, "sacks": 0.8}},
        {"name": "Derek Stingley Jr.", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 4.8, "interceptions": 0.3}},
    ],
    
    # Cleveland Browns
    "Cleveland Browns": [
        # Offense
        {"name": "Deshaun Watson", "position": "QB", "type": "offense", "stats": {"yards_per_game": 240, "touchdowns": 1.8}},
        {"name": "Nick Chubb", "position": "RB", "type": "offense", "stats": {"yards_per_game": 95, "touchdowns": 0.8}},
        {"name": "Amari Cooper", "position": "WR", "type": "offense", "stats": {"yards_per_game": 75, "touchdowns": 0.6}},
        {"name": "David Njoku", "position": "TE", "type": "offense", "stats": {"yards_per_game": 50, "touchdowns": 0.4}},
        {"name": "Elijah Moore", "position": "WR", "type": "offense", "stats": {"yards_per_game": 40, "touchdowns": 0.3}},
        # Defense
        {"name": "Myles Garrett", "position": "DE", "type": "defense", "stats": {"tackles_per_game": 5.5, "sacks": 1.2}},
        {"name": "Jeremiah Owusu-Koramoah", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 7.5, "sacks": 0.4}},
        {"name": "Denzel Ward", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 4.2, "interceptions": 0.2}},
    ],
    
    # Pittsburgh Steelers
    "Pittsburgh Steelers": [
        # Offense
        {"name": "Kenny Pickett", "position": "QB", "type": "offense", "stats": {"yards_per_game": 220, "touchdowns": 1.5}},
        {"name": "Najee Harris", "position": "RB", "type": "offense", "stats": {"yards_per_game": 70, "touchdowns": 0.5}},
        {"name": "Diontae Johnson", "position": "WR", "type": "offense", "stats": {"yards_per_game": 65, "touchdowns": 0.5}},
        {"name": "George Pickens", "position": "WR", "type": "offense", "stats": {"yards_per_game": 60, "touchdowns": 0.5}},
        {"name": "Pat Freiermuth", "position": "TE", "type": "offense", "stats": {"yards_per_game": 45, "touchdowns": 0.4}},
        # Defense
        {"name": "T.J. Watt", "position": "OLB", "type": "defense", "stats": {"tackles_per_game": 5.8, "sacks": 1.1}},
        {"name": "Minkah Fitzpatrick", "position": "S", "type": "defense", "stats": {"tackles_per_game": 6.5, "interceptions": 0.3}},
        {"name": "Cameron Heyward", "position": "DT", "type": "defense", "stats": {"tackles_per_game": 4.2, "sacks": 0.6}},
    ],
    
    # Los Angeles Chargers
    "Los Angeles Chargers": [
        # Offense
        {"name": "Justin Herbert", "position": "QB", "type": "offense", "stats": {"yards_per_game": 280, "touchdowns": 2.2}},
        {"name": "Keenan Allen", "position": "WR", "type": "offense", "stats": {"yards_per_game": 90, "touchdowns": 0.8}},
        {"name": "Austin Ekeler", "position": "RB", "type": "offense", "stats": {"yards_per_game": 80, "touchdowns": 0.7}},
        {"name": "Mike Williams", "position": "WR", "type": "offense", "stats": {"yards_per_game": 65, "touchdowns": 0.6}},
        {"name": "Gerald Everett", "position": "TE", "type": "offense", "stats": {"yards_per_game": 40, "touchdowns": 0.3}},
        # Defense
        {"name": "Khalil Mack", "position": "OLB", "type": "defense", "stats": {"tackles_per_game": 5.2, "sacks": 0.9}},
        {"name": "Derwin James", "position": "S", "type": "defense", "stats": {"tackles_per_game": 7.2, "interceptions": 0.2}},
        {"name": "Joey Bosa", "position": "DE", "type": "defense", "stats": {"tackles_per_game": 4.5, "sacks": 0.7}},
    ],
    
    # Seattle Seahawks
    "Seattle Seahawks": [
        # Offense
        {"name": "Geno Smith", "position": "QB", "type": "offense", "stats": {"yards_per_game": 250, "touchdowns": 1.9}},
        {"name": "DK Metcalf", "position": "WR", "type": "offense", "stats": {"yards_per_game": 80, "touchdowns": 0.7}},
        {"name": "Tyler Lockett", "position": "WR", "type": "offense", "stats": {"yards_per_game": 70, "touchdowns": 0.6}},
        {"name": "Kenneth Walker III", "position": "RB", "type": "offense", "stats": {"yards_per_game": 75, "touchdowns": 0.6}},
        {"name": "Noah Fant", "position": "TE", "type": "offense", "stats": {"yards_per_game": 35, "touchdowns": 0.3}},
        # Defense
        {"name": "Bobby Wagner", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 9.5, "sacks": 0.2}},
        {"name": "Quandre Diggs", "position": "S", "type": "defense", "stats": {"tackles_per_game": 6.2, "interceptions": 0.3}},
        {"name": "Jordyn Brooks", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 8.2, "sacks": 0.3}},
    ],
    
    # New York Jets
    "New York Jets": [
        # Offense
        {"name": "Aaron Rodgers", "position": "QB", "type": "offense", "stats": {"yards_per_game": 260, "touchdowns": 2.0}},
        {"name": "Garrett Wilson", "position": "WR", "type": "offense", "stats": {"yards_per_game": 75, "touchdowns": 0.6}},
        {"name": "Breece Hall", "position": "RB", "type": "offense", "stats": {"yards_per_game": 85, "touchdowns": 0.7}},
        {"name": "Allen Lazard", "position": "WR", "type": "offense", "stats": {"yards_per_game": 45, "touchdowns": 0.4}},
        {"name": "Tyler Conklin", "position": "TE", "type": "offense", "stats": {"yards_per_game": 35, "touchdowns": 0.3}},
        # Defense
        {"name": "Quinnen Williams", "position": "DT", "type": "defense", "stats": {"tackles_per_game": 4.8, "sacks": 0.7}},
        {"name": "C.J. Mosley", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 8.8, "sacks": 0.2}},
        {"name": "Sauce Gardner", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 4.5, "interceptions": 0.3}},
    ],
    
    # Tampa Bay Buccaneers
    "Tampa Bay Buccaneers": [
        # Offense
        {"name": "Baker Mayfield", "position": "QB", "type": "offense", "stats": {"yards_per_game": 250, "touchdowns": 1.9}},
        {"name": "Mike Evans", "position": "WR", "type": "offense", "stats": {"yards_per_game": 75, "touchdowns": 0.7}},
        {"name": "Chris Godwin", "position": "WR", "type": "offense", "stats": {"yards_per_game": 70, "touchdowns": 0.6}},
        {"name": "Rachaad White", "position": "RB", "type": "offense", "stats": {"yards_per_game": 70, "touchdowns": 0.5}},
        {"name": "Cade Otton", "position": "TE", "type": "offense", "stats": {"yards_per_game": 30, "touchdowns": 0.3}},
        # Defense
        {"name": "Lavonte David", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 8.5, "sacks": 0.3}},
        {"name": "Vita Vea", "position": "DT", "type": "defense", "stats": {"tackles_per_game": 3.8, "sacks": 0.5}},
        {"name": "Antoine Winfield Jr.", "position": "S", "type": "defense", "stats": {"tackles_per_game": 7.2, "interceptions": 0.3}},
    ],
    
    # Atlanta Falcons
    "Atlanta Falcons": [
        # Offense
        {"name": "Desmond Ridder", "position": "QB", "type": "offense", "stats": {"yards_per_game": 220, "touchdowns": 1.6}},
        {"name": "Bijan Robinson", "position": "RB", "type": "offense", "stats": {"yards_per_game": 90, "touchdowns": 0.7}},
        {"name": "Drake London", "position": "WR", "type": "offense", "stats": {"yards_per_game": 70, "touchdowns": 0.6}},
        {"name": "Kyle Pitts", "position": "TE", "type": "offense", "stats": {"yards_per_game": 55, "touchdowns": 0.5}},
        {"name": "Mack Hollins", "position": "WR", "type": "offense", "stats": {"yards_per_game": 40, "touchdowns": 0.3}},
        # Defense
        {"name": "Grady Jarrett", "position": "DT", "type": "defense", "stats": {"tackles_per_game": 4.2, "sacks": 0.6}},
        {"name": "Jessie Bates III", "position": "S", "type": "defense", "stats": {"tackles_per_game": 7.5, "interceptions": 0.4}},
        {"name": "A.J. Terrell", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 5.2, "interceptions": 0.2}},
    ],
    
    # Los Angeles Rams
    "Los Angeles Rams": [
        # Offense
        {"name": "Matthew Stafford", "position": "QB", "type": "offense", "stats": {"yards_per_game": 270, "touchdowns": 2.0}},
        {"name": "Cooper Kupp", "position": "WR", "type": "offense", "stats": {"yards_per_game": 85, "touchdowns": 0.8}},
        {"name": "Puka Nacua", "position": "WR", "type": "offense", "stats": {"yards_per_game": 90, "touchdowns": 0.7}},
        {"name": "Kyren Williams", "position": "RB", "type": "offense", "stats": {"yards_per_game": 80, "touchdowns": 0.7}},
        {"name": "Tyler Higbee", "position": "TE", "type": "offense", "stats": {"yards_per_game": 40, "touchdowns": 0.3}},
        # Defense
        {"name": "Aaron Donald", "position": "DT", "type": "defense", "stats": {"tackles_per_game": 4.5, "sacks": 0.8}},
        {"name": "Ernest Jones", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 7.8, "sacks": 0.3}},
        {"name": "Derion Kendrick", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 4.8, "interceptions": 0.2}},
    ],
    
    # New Orleans Saints
    "New Orleans Saints": [
        # Offense
        {"name": "Derek Carr", "position": "QB", "type": "offense", "stats": {"yards_per_game": 240, "touchdowns": 1.8}},
        {"name": "Alvin Kamara", "position": "RB", "type": "offense", "stats": {"yards_per_game": 75, "touchdowns": 0.6}},
        {"name": "Chris Olave", "position": "WR", "type": "offense", "stats": {"yards_per_game": 80, "touchdowns": 0.7}},
        {"name": "Rashid Shaheed", "position": "WR", "type": "offense", "stats": {"yards_per_game": 50, "touchdowns": 0.4}},
        {"name": "Juwan Johnson", "position": "TE", "type": "offense", "stats": {"yards_per_game": 35, "touchdowns": 0.3}},
        # Defense
        {"name": "Cameron Jordan", "position": "DE", "type": "defense", "stats": {"tackles_per_game": 4.8, "sacks": 0.7}},
        {"name": "Demario Davis", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 8.5, "sacks": 0.3}},
        {"name": "Tyrann Mathieu", "position": "S", "type": "defense", "stats": {"tackles_per_game": 6.8, "interceptions": 0.3}},
    ],
    
    # Arizona Cardinals
    "Arizona Cardinals": [
        # Offense
        {"name": "Kyler Murray", "position": "QB", "type": "offense", "stats": {"yards_per_game": 250, "touchdowns": 1.9}},
        {"name": "James Conner", "position": "RB", "type": "offense", "stats": {"yards_per_game": 75, "touchdowns": 0.6}},
        {"name": "Marquise Brown", "position": "WR", "type": "offense", "stats": {"yards_per_game": 70, "touchdowns": 0.6}},
        {"name": "Trey McBride", "position": "TE", "type": "offense", "stats": {"yards_per_game": 50, "touchdowns": 0.4}},
        {"name": "Rondale Moore", "position": "WR", "type": "offense", "stats": {"yards_per_game": 40, "touchdowns": 0.3}},
        # Defense
        {"name": "Zaven Collins", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 7.2, "sacks": 0.4}},
        {"name": "Budda Baker", "position": "S", "type": "defense", "stats": {"tackles_per_game": 7.5, "interceptions": 0.2}},
        {"name": "Marco Wilson", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 4.5, "interceptions": 0.2}},
    ],
    
    # Carolina Panthers
    "Carolina Panthers": [
        # Offense
        {"name": "Bryce Young", "position": "QB", "type": "offense", "stats": {"yards_per_game": 210, "touchdowns": 1.4}},
        {"name": "Chuba Hubbard", "position": "RB", "type": "offense", "stats": {"yards_per_game": 65, "touchdowns": 0.5}},
        {"name": "Adam Thielen", "position": "WR", "type": "offense", "stats": {"yards_per_game": 70, "touchdowns": 0.6}},
        {"name": "Jonathan Mingo", "position": "WR", "type": "offense", "stats": {"yards_per_game": 40, "touchdowns": 0.3}},
        {"name": "Hayden Hurst", "position": "TE", "type": "offense", "stats": {"yards_per_game": 35, "touchdowns": 0.3}},
        # Defense
        {"name": "Brian Burns", "position": "OLB", "type": "defense", "stats": {"tackles_per_game": 5.2, "sacks": 0.8}},
        {"name": "Derrick Brown", "position": "DT", "type": "defense", "stats": {"tackles_per_game": 4.5, "sacks": 0.5}},
        {"name": "Jaycee Horn", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 4.8, "interceptions": 0.2}},
    ],
    
    # Washington Commanders
    "Washington Commanders": [
        # Offense
        {"name": "Sam Howell", "position": "QB", "type": "offense", "stats": {"yards_per_game": 240, "touchdowns": 1.8}},
        {"name": "Terry McLaurin", "position": "WR", "type": "offense", "stats": {"yards_per_game": 75, "touchdowns": 0.6}},
        {"name": "Brian Robinson Jr.", "position": "RB", "type": "offense", "stats": {"yards_per_game": 70, "touchdowns": 0.5}},
        {"name": "Curtis Samuel", "position": "WR", "type": "offense", "stats": {"yards_per_game": 50, "touchdowns": 0.4}},
        {"name": "Logan Thomas", "position": "TE", "type": "offense", "stats": {"yards_per_game": 35, "touchdowns": 0.3}},
        # Defense
        {"name": "Chase Young", "position": "DE", "type": "defense", "stats": {"tackles_per_game": 4.8, "sacks": 0.7}},
        {"name": "Jonathan Allen", "position": "DT", "type": "defense", "stats": {"tackles_per_game": 4.2, "sacks": 0.6}},
        {"name": "Kendall Fuller", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 5.0, "interceptions": 0.2}},
    ],
    
    # New York Giants
    "New York Giants": [
        # Offense
        {"name": "Daniel Jones", "position": "QB", "type": "offense", "stats": {"yards_per_game": 220, "touchdowns": 1.5}},
        {"name": "Saquon Barkley", "position": "RB", "type": "offense", "stats": {"yards_per_game": 85, "touchdowns": 0.7}},
        {"name": "Darius Slayton", "position": "WR", "type": "offense", "stats": {"yards_per_game": 60, "touchdowns": 0.5}},
        {"name": "Darren Waller", "position": "TE", "type": "offense", "stats": {"yards_per_game": 50, "touchdowns": 0.4}},
        {"name": "Wan'Dale Robinson", "position": "WR", "type": "offense", "stats": {"yards_per_game": 40, "touchdowns": 0.3}},
        # Defense
        {"name": "Kayvon Thibodeaux", "position": "OLB", "type": "defense", "stats": {"tackles_per_game": 5.5, "sacks": 0.8}},
        {"name": "Dexter Lawrence", "position": "DT", "type": "defense", "stats": {"tackles_per_game": 4.5, "sacks": 0.6}},
        {"name": "Xavier McKinney", "position": "S", "type": "defense", "stats": {"tackles_per_game": 6.5, "interceptions": 0.2}},
    ],
    
    # Chicago Bears
    "Chicago Bears": [
        # Offense
        {"name": "Justin Fields", "position": "QB", "type": "offense", "stats": {"yards_per_game": 230, "touchdowns": 1.7}},
        {"name": "D.J. Moore", "position": "WR", "type": "offense", "stats": {"yards_per_game": 80, "touchdowns": 0.7}},
        {"name": "Khalil Herbert", "position": "RB", "type": "offense", "stats": {"yards_per_game": 70, "touchdowns": 0.5}},
        {"name": "Cole Kmet", "position": "TE", "type": "offense", "stats": {"yards_per_game": 45, "touchdowns": 0.4}},
        {"name": "Darnell Mooney", "position": "WR", "type": "offense", "stats": {"yards_per_game": 40, "touchdowns": 0.3}},
        # Defense
        {"name": "Montez Sweat", "position": "DE", "type": "defense", "stats": {"tackles_per_game": 4.8, "sacks": 0.7}},
        {"name": "Tremaine Edmunds", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 8.2, "sacks": 0.3}},
        {"name": "Jaylon Johnson", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 5.2, "interceptions": 0.3}},
    ],
    
    # Minnesota Vikings
    "Minnesota Vikings": [
        # Offense
        {"name": "Kirk Cousins", "position": "QB", "type": "offense", "stats": {"yards_per_game": 270, "touchdowns": 2.1}},
        {"name": "Justin Jefferson", "position": "WR", "type": "offense", "stats": {"yards_per_game": 110, "touchdowns": 1.0}},
        {"name": "T.J. Hockenson", "position": "TE", "type": "offense", "stats": {"yards_per_game": 70, "touchdowns": 0.6}},
        {"name": "Alexander Mattison", "position": "RB", "type": "offense", "stats": {"yards_per_game": 65, "touchdowns": 0.5}},
        {"name": "Jordan Addison", "position": "WR", "type": "offense", "stats": {"yards_per_game": 60, "touchdowns": 0.5}},
        # Defense
        {"name": "Danielle Hunter", "position": "OLB", "type": "defense", "stats": {"tackles_per_game": 5.2, "sacks": 0.9}},
        {"name": "Harrison Smith", "position": "S", "type": "defense", "stats": {"tackles_per_game": 7.0, "interceptions": 0.3}},
        {"name": "Byron Murphy Jr.", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 5.0, "interceptions": 0.2}},
    ],
    
    # Las Vegas Raiders
    "Las Vegas Raiders": [
        # Offense
        {"name": "Aidan O'Connell", "position": "QB", "type": "offense", "stats": {"yards_per_game": 230, "touchdowns": 1.6}},
        {"name": "Davante Adams", "position": "WR", "type": "offense", "stats": {"yards_per_game": 85, "touchdowns": 0.7}},
        {"name": "Josh Jacobs", "position": "RB", "type": "offense", "stats": {"yards_per_game": 80, "touchdowns": 0.6}},
        {"name": "Jakobi Meyers", "position": "WR", "type": "offense", "stats": {"yards_per_game": 55, "touchdowns": 0.4}},
        {"name": "Michael Mayer", "position": "TE", "type": "offense", "stats": {"yards_per_game": 35, "touchdowns": 0.3}},
        # Defense
        {"name": "Maxx Crosby", "position": "DE", "type": "defense", "stats": {"tackles_per_game": 5.8, "sacks": 1.0}},
        {"name": "Robert Spillane", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 8.5, "sacks": 0.2}},
        {"name": "Marcus Peters", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 4.8, "interceptions": 0.3}},
    ],
    
    # Denver Broncos
    "Denver Broncos": [
        # Offense
        {"name": "Russell Wilson", "position": "QB", "type": "offense", "stats": {"yards_per_game": 240, "touchdowns": 1.8}},
        {"name": "Courtland Sutton", "position": "WR", "type": "offense", "stats": {"yards_per_game": 70, "touchdowns": 0.6}},
        {"name": "Javonte Williams", "position": "RB", "type": "offense", "stats": {"yards_per_game": 70, "touchdowns": 0.5}},
        {"name": "Jerry Jeudy", "position": "WR", "type": "offense", "stats": {"yards_per_game": 55, "touchdowns": 0.4}},
        {"name": "Adam Trautman", "position": "TE", "type": "offense", "stats": {"yards_per_game": 30, "touchdowns": 0.2}},
        # Defense
        {"name": "Patrick Surtain II", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 5.2, "interceptions": 0.3}},
        {"name": "Justin Simmons", "position": "S", "type": "defense", "stats": {"tackles_per_game": 7.2, "interceptions": 0.4}},
        {"name": "Baron Browning", "position": "OLB", "type": "defense", "stats": {"tackles_per_game": 4.5, "sacks": 0.6}},
    ],
    
    # Tennessee Titans
    "Tennessee Titans": [
        # Offense
        {"name": "Will Levis", "position": "QB", "type": "offense", "stats": {"yards_per_game": 220, "touchdowns": 1.6}},
        {"name": "Derrick Henry", "position": "RB", "type": "offense", "stats": {"yards_per_game": 85, "touchdowns": 0.7}},
        {"name": "DeAndre Hopkins", "position": "WR", "type": "offense", "stats": {"yards_per_game": 70, "touchdowns": 0.6}},
        {"name": "Treylon Burks", "position": "WR", "type": "offense", "stats": {"yards_per_game": 40, "touchdowns": 0.3}},
        {"name": "Chigoziem Okonkwo", "position": "TE", "type": "offense", "stats": {"yards_per_game": 35, "touchdowns": 0.3}},
        # Defense
        {"name": "Jeffery Simmons", "position": "DT", "type": "defense", "stats": {"tackles_per_game": 4.5, "sacks": 0.7}},
        {"name": "Azeez Al-Shaair", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 8.2, "sacks": 0.3}},
        {"name": "Kevin Byard", "position": "S", "type": "defense", "stats": {"tackles_per_game": 6.5, "interceptions": 0.3}},
    ],
    
    # Jacksonville Jaguars
    "Jacksonville Jaguars": [
        # Offense
        {"name": "Trevor Lawrence", "position": "QB", "type": "offense", "stats": {"yards_per_game": 265, "touchdowns": 2.0}},
        {"name": "Travis Etienne", "position": "RB", "type": "offense", "stats": {"yards_per_game": 80, "touchdowns": 0.7}},
        {"name": "Calvin Ridley", "position": "WR", "type": "offense", "stats": {"yards_per_game": 75, "touchdowns": 0.6}},
        {"name": "Evan Engram", "position": "TE", "type": "offense", "stats": {"yards_per_game": 60, "touchdowns": 0.5}},
        {"name": "Christian Kirk", "position": "WR", "type": "offense", "stats": {"yards_per_game": 55, "touchdowns": 0.4}},
        # Defense
        {"name": "Josh Allen", "position": "OLB", "type": "defense", "stats": {"tackles_per_game": 5.2, "sacks": 0.8}},
        {"name": "Foyesade Oluokun", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 9.5, "sacks": 0.2}},
        {"name": "Tyson Campbell", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 5.0, "interceptions": 0.2}},
    ],
    
    # Indianapolis Colts
    "Indianapolis Colts": [
        # Offense
        {"name": "Anthony Richardson", "position": "QB", "type": "offense", "stats": {"yards_per_game": 230, "touchdowns": 1.7}},
        {"name": "Jonathan Taylor", "position": "RB", "type": "offense", "stats": {"yards_per_game": 90, "touchdowns": 0.8}},
        {"name": "Michael Pittman Jr.", "position": "WR", "type": "offense", "stats": {"yards_per_game": 75, "touchdowns": 0.6}},
        {"name": "Josh Downs", "position": "WR", "type": "offense", "stats": {"yards_per_game": 50, "touchdowns": 0.4}},
        {"name": "Mo Alie-Cox", "position": "TE", "type": "offense", "stats": {"yards_per_game": 25, "touchdowns": 0.2}},
        # Defense
        {"name": "DeForest Buckner", "position": "DT", "type": "defense", "stats": {"tackles_per_game": 4.8, "sacks": 0.7}},
        {"name": "Zaire Franklin", "position": "LB", "type": "defense", "stats": {"tackles_per_game": 9.2, "sacks": 0.2}},
        {"name": "Kenny Moore II", "position": "CB", "type": "defense", "stats": {"tackles_per_game": 5.5, "interceptions": 0.2}},
    ],
}

def get_all_nfl_players() -> List[Dict]:
    """
    Get all NFL players (offensive and defensive) from all teams
    
    Returns:
        List of all players with team, position, type, and stats
    """
    all_players = []
    for team, players in NFL_PLAYERS.items():
        for player in players:
            player_with_team = {
                "name": player["name"],
                "team": team,
                "position": player["position"],
                "type": player["type"],
                "stats": player["stats"]
            }
            all_players.append(player_with_team)
    return all_players

def get_players_by_type(player_type: str = "all") -> List[Dict]:
    """
    Get players filtered by type (offense, defense, or all)
    
    Args:
        player_type: "offense", "defense", or "all"
    
    Returns:
        Filtered list of players
    """
    all_players = get_all_nfl_players()
    if player_type == "all":
        return all_players
    return [p for p in all_players if p["type"] == player_type]

def search_players(query: str, player_type: str = "all") -> List[Dict]:
    """
    Search for players by name or team
    
    Args:
        query: Search query
        player_type: "offense", "defense", or "all"
    
    Returns:
        List of matching players
    """
    players = get_players_by_type(player_type)
    if not query:
        return players
    
    query_lower = query.lower()
    return [
        p for p in players
        if query_lower in p["name"].lower() or query_lower in p["team"].lower()
    ]


