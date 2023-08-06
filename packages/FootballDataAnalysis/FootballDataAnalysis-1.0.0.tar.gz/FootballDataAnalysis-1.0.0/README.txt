# Football Data Analysis Project
Project by Bohdan Yatskiv for my coursework at UCU.

Application allows to get statistics for each team from following leagues:

 - Premier League(ENG)
 - La Liga(ESP)
 - Bundesliga(GER)
 - Serie A(ITA)
 - Ligue 1(FRA)

## Description
This program allows you to get detailed statistics like average goals per game, home and away statistics, wins percentage
for any team from top 5 leagues and compare it with other teams. 

## Input and output
The program input is name of the league and team name.
The output is statistics data.

## Modules description
* main.py - main module that runs the program
   - class Menu - helps to control the program by user input comands
* classes.py - module that contains data structure classes
   - class League 
   - class Team
* adt.py - module with ADT
   - class MatchList
      - choose_league
      - get_standings
      - get_scorers
      - get_matchday
      - choose_team
      - get_stats
      - compare
   
* updater.py - module that updates .json files with all necessary data

## Usage
1.Run main.py module and choose a league from the list(example: Premier League)

2.You will recieve menu with following commands:
 * get standings - league table
 * get scorers - list of league top 10 scorers
 * get matchday - all matches of chosen matchday 
 * choose a team 
 * choose another league
 * quit

3. If you enter "choose a team" command you will recieve following team menu:
 * get stats - team statisctics
 * compare - compare two teams statistics
 * back - return to previous menu 
 
 ## Test examples
 Team statistics example:
 
    Team name: Liverpool FC
    Position: 2
    OVERALL statistics:
    Wins - 29(78.4%) Draws - 7(18.9%) Loses - 1(2.7%)
    Goals scored - 87
    Goals missed - 22
    Goals per game scored(average) - 2.35
    Goals per game missed(average) - 0.59
    Statistics against top 6 teams:
    Wins - 5 Draws - 4 Loses - 1
    ---------------------------------------------
    HOME statistics:
    Wins - 16(88.9%) Draws - 2(11.1%) Loses - 0(0.0%)
    Goals scored - 53
    Goals missed - 10
    Goals per game scored(average) - 2.94
    Goals per game missed(average) - 0.56
    ---------------------------------------------
    AWAY statistics:
    Wins - 13(68.4%) Draws - 5(26.3%) Loses - 1(5.3%)
    Goals scored - 34
    Goals missed - 12
    Goals per game scored(average) - 1.79
    Goals per game missed(average) - 0.63
    ---------------------------------------------
    FORM(Last 5 games):
    Southampton FC 1-3 Liverpool FC
    Liverpool FC 2-0 Chelsea FC
    Cardiff City FC 0-2 Liverpool FC
    Liverpool FC 5-0 Huddersfield Town AFC
    Newcastle United FC 2-3 Liverpool FC
Standings example:

    Premier League
    № Name                        G  W  D  L  GF  GA  GD   P
     1 Manchester City FC         37 31  2  4  91  22  69  95
     2 Liverpool FC               37 29  7  1  87  22  65  94
     3 Chelsea FC                 37 21  8  8  63  39  24  71
     4 Tottenham Hotspur FC       37 23  1 13  65  37  28  70
     5 Arsenal FC                 37 20  7 10  70  50  20  67
     6 Manchester United FC       37 19  9  9  65  52  13  66
     7 Wolverhampton Wanderers FC 37 16  9 12  47  44   3  57
     8 Everton FC                 37 15  8 14  52  44   8  53
     9 Leicester City FC          37 15  6 16  51  48   3  51
    10 Watford FC                 37 14  8 15  51  55  -4  50
    11 West Ham United FC         37 14  7 16  48  54  -6  49
    12 Crystal Palace FC          37 13  7 17  46  50  -4  46
    13 AFC Bournemouth            37 13  6 18  53  65 -12  45
    14 Newcastle United FC        37 11  9 17  38  48 -10  42
    15 Burnley FC                 37 11  7 19  44  65 -21  40
    16 Southampton FC             37  9 11 17  44  64 -20  38
    17 Brighton & Hove Albion FC  37  9  9 19  34  56 -22  36
    18 Cardiff City FC            37  9  4 24  32  69 -37  31
    19 Fulham FC                  37  7  5 25  34  77 -43  26
    20 Huddersfield Town AFC      37  3  6 28  21  75 -54  15

Two teams comparison example:

                    FC Barcelona                    Real Madrid CF
                            1       position        3
    25(69.4%)-8(22.2%)-3(8.3%)      stat            21(58.3%)-5(13.9%)-10(27.8%)
    14(77.8%)-3(16.7%)-1(5.6%)      home stat       13(72.2%)-1(5.6%)-4(22.2%)
    11(61.1%)-5(27.8%)-2(11.1%)     away stat       8(44.4%)-4(22.2%)-6(33.3%)
                            86      goals scored    62
                            34      goals missed    41
                            2.39    avg scored      1.72
                            0.94    avg missed      1.14
    Please enter a command:

            get stats---Get detailed team statistics
            compare---Compare two teams head to head
            back---Go back to previous page                        
                        

#### This page could be changed, as project is still in development.
