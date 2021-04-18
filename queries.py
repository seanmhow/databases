def severityToStorm(minutes='60',state='All'):
    #Accident severity grouped by storm
    #Display as bar plot
    if state != 'All':
        return f"""SELECT stormtype, AVG(Severity) as Severity FROM(
        SELECT stormtype, Severity FROM JPalavec.Accident A
        Join JPalavec.Storm S ON A.county = S.county AND A.state = S.state
        WHERE (A.startdate > S.begindate AND A.startdate < S.begindate + interval '{minutes}' minute )
        OR (A.enddate > S.begindate AND A.enddate < S.begindate + interval '{minutes}' minute))
        AND A.state = '{state}'
        GROUP BY stormtype"""
    return f"""SELECT stormtype, AVG(Severity) as Severity FROM(
    SELECT stormtype, Severity FROM JPalavec.Accident A
    Join JPalavec.Storm S ON A.county = S.county AND A.state = S.state
    WHERE (A.startdate > S.begindate AND A.startdate < S.begindate + interval '{minutes}' minute )
    OR (A.enddate > S.begindate AND A.enddate < S.begindate + interval '{minutes}' minute))
    GROUP BY stormtype"""

def accidentDurationToStorm(minutes='60',state='All'):
 #User selects storm duration, accident duration grouped by storm
 #Display as bar plot
    if state != 'All':
        return f"""SELECT stormtype, AVG(24 *60* extract(day FROM ENDDATE - STARTDATE) + 60*extract(hour from ENDDATE - STARTDATE) + extract(minute from ENDDATE - STARTDATE)) as Duration FROM(
                SELECT stormtype, A.startdate, A.enddate FROM JPalavec.Accident A
                Join JPalavec.Storm S ON A.county = S.county AND A.state = S.state
                WHERE (A.startdate > S.begindate AND A.startdate < S.begindate + interval '{minutes}' minute )
                OR (A.enddate > S.begindate AND A.enddate < S.begindate + interval '{minutes}' minute))
                AND A.state = '{state}'
                GROUP BY stormtype"""
    return f"""SELECT stormtype, AVG(24 *60* extract(day FROM ENDDATE - STARTDATE) + 60*extract(hour from ENDDATE - STARTDATE) + extract(minute from ENDDATE - STARTDATE)) as Duration FROM(
                SELECT stormtype, A.startdate, A.enddate FROM JPalavec.Accident A
                Join JPalavec.Storm S ON A.county = S.county AND A.state = S.state
                WHERE (A.startdate > S.begindate AND A.startdate < S.begindate + interval '{minutes}' minute )
                OR (A.enddate > S.begindate AND A.enddate < S.begindate + interval '{minutes}' minute))
                GROUP BY stormtype"""

def stormAccidentDurationVsAverage(minutes='60', stormtype='All'):
    #returns 2 values, one is accidents during stormtype, other is average accidents. Can do barplot (or other option if you think of something better)
    if stormtype != 'All':
        return f"""SELECT SDuration, Duration
                FROM
                (SELECT AVG(24 *60* extract(day FROM ENDDATE - STARTDATE) + 60*extract(hour from ENDDATE - STARTDATE) + extract(minute from ENDDATE - STARTDATE)) as SDuration FROM(
                SELECT A.startdate, A.enddate FROM JPalavec.Accident A
                Join JPalavec.Storm S ON A.county = S.county AND A.state = S.state
                WHERE (A.startdate > S.begindate AND A.startdate < S.begindate + interval '{minutes}' minute AND S.stormtype = '{stormtype}')
                OR (A.enddate > S.begindate AND A.enddate < S.begindate + interval '{minutes}' minute))),
                (SELECT AVG(24 *60* extract(day FROM ENDDATE - STARTDATE) + 60*extract(hour from ENDDATE - STARTDATE) + extract(minute from ENDDATE - STARTDATE)) as Duration
                FROM JPalavec.Accident)"""
    return f"""SELECT SDuration, Duration
        FROM
        (SELECT AVG(24 *60* extract(day FROM ENDDATE - STARTDATE) + 60*extract(hour from ENDDATE - STARTDATE) + extract(minute from ENDDATE - STARTDATE)) as SDuration FROM(
        SELECT A.startdate, A.enddate FROM JPalavec.Accident A
        Join JPalavec.Storm S ON A.county = S.county AND A.state = S.state
        WHERE (A.startdate > S.begindate AND A.startdate < S.begindate + interval '{minutes}' minute)
        OR (A.enddate > S.begindate AND A.enddate < S.begindate + interval '{minutes}' minute))),
        (SELECT AVG(24 *60* extract(day FROM ENDDATE - STARTDATE) + 60*extract(hour from ENDDATE - STARTDATE) + extract(minute from ENDDATE - STARTDATE)) as Duration
        FROM JPalavec.Accident)"""


def hourMonthHeatmap(state='All',county='All'):
    #Heatmap, user can optionall select County and State with default value of All
    if state != 'All':
        if county != 'All':
            return f"""SELECT Count(*) as Counts, Hour, Month
                FROM
                (
                SELECT EXTRACT(HOUR FROM StartDate) as Hour,EXTRACT(MONTH FROM StartDate) as Month
                FROM JPalavec.Accident
                WHERE state = '{state}' AND county='{county}'
                )
                GROUP BY Hour, Month"""
        return f"""SELECT Count(*) as Counts, Hour, Month
                FROM
                (
                SELECT EXTRACT(HOUR FROM StartDate) as Hour,EXTRACT(MONTH FROM StartDate) as Month
                FROM JPalavec.Accident
                WHERE state = '{state}'
                )
                GROUP BY Hour, Month"""
    return f"""SELECT Count(*) as Counts, Hour, Month
                FROM
                (
                SELECT EXTRACT(HOUR FROM StartDate) as Hour,EXTRACT(MONTH FROM StartDate) as Month
                FROM JPalavec.Accident
                )
                GROUP BY Hour, Month"""

def hourAverageDensityHeatmap(state="All"):
    if state != 'All':
        f"""SELECT Count(*) as Counts, Hour, AverageDensity
        FROM
        (SELECT EXTRACT(HOUR FROM StartDate) as Hour, AverageDensity
        FROM
        (SELECT AVG(PopDensity) as AverageDensity, Poptile
        FROM
        (SELECT county, state, Pop2018 / LandArea as PopDensity, NTILE(10) OVER (ORDER BY Pop2018 / landArea) AS PopTile
        FROM  JPalavec.County C
        WHERE county != 'All' AND state = '{state}'
        )GROUP BY PopTile) C1,
        (SELECT county, state, Pop2018 / LandArea as PopDensity, NTILE(10) OVER (ORDER BY Pop2018 / landArea) AS PopTile
        FROM  JPalavec.County C
        WHERE county != 'All' AND state = '{state}') C2,
        JPalavec.Accident A
        WHERE C1.poptile = C2.Poptile AND A.county = C2.county AND A.state = C2.state)
        GROUP BY Hour, AverageDensity"""
    return f"""SELECT Count(*) as Counts, Hour, AverageDensity
            FROM
            (SELECT EXTRACT(HOUR FROM StartDate) as Hour, AverageDensity
            FROM
            (SELECT AVG(PopDensity) as AverageDensity, Poptile
            FROM
            (SELECT county, state, Pop2018 / LandArea as PopDensity, NTILE(10) OVER (ORDER BY Pop2018 / landArea) AS PopTile
            FROM  JPalavec.County C
            WHERE county != 'All'
            )GROUP BY PopTile) C1,
            (SELECT county, state, Pop2018 / LandArea as PopDensity, NTILE(10) OVER (ORDER BY Pop2018 / landArea) AS PopTile
            FROM  JPalavec.County C
            WHERE county != 'All') C2,
            JPalavec.Accident A
            WHERE C1.poptile = C2.Poptile AND A.county = C2.county AND A.state = C2.state)
            GROUP BY Hour, AverageDensity"""

def accidentDurationHourHeatmap(state='All',county="All"):
    if (state != 'All'):
        if (county != 'All'):
            return f"""WITH Durations AS (SELECT AID,StartDate,24 *60* extract(day FROM ENDDATE - STARTDATE) + 60*extract(hour from ENDDATE - STARTDATE) + extract(minute from ENDDATE - STARTDATE) as Duration
            FROM JPalavec.Accident
            WHERE state = '{state}' AND county= '{county}')
            SELECT Count(*) as Counts, Hour, AverageDuration /*Format in correct form for Python heatmap*/
            FROM
            (SELECT EXTRACT(HOUR FROM StartDate) as Hour, AverageDuration 
            FROM
            (SELECT AVG(Duration) as AverageDuration, DurPercentile   /*Gets average duration of each DurPercentile*/
            FROM
            (SELECT Duration, NTILE(10) OVER (ORDER BY Duration) AS DurPercentile 
            FROM Durations
            )GROUP BY DurPercentile) A1,
            (SELECT AID,StartDate,Duration, NTILE(10) OVER (ORDER BY Duration) AS DurPercentile /*Gets all information and combines it with DurPercentile*/
            FROM  Durations
            ) A2
            WHERE A1.DurPercentile = A2.DurPercentile)
            GROUP BY Hour, AverageDuration
            ORDER BY Counts desc"""
        return f"""WITH Durations AS (SELECT AID,StartDate,24 *60* extract(day FROM ENDDATE - STARTDATE) + 60*extract(hour from ENDDATE - STARTDATE) + extract(minute from ENDDATE - STARTDATE) as Duration
            FROM JPalavec.Accident
            WHERE state = '{state}')
            SELECT Count(*) as Counts, Hour, AverageDuration /*Format in correct form for Python heatmap*/
            FROM
            (SELECT EXTRACT(HOUR FROM StartDate) as Hour, AverageDuration 
            FROM
            (SELECT AVG(Duration) as AverageDuration, DurPercentile   /*Gets average duration of each DurPercentile*/
            FROM
            (SELECT Duration, NTILE(10) OVER (ORDER BY Duration) AS DurPercentile 
            FROM Durations
            )GROUP BY DurPercentile) A1,
            (SELECT AID,StartDate,Duration, NTILE(10) OVER (ORDER BY Duration) AS DurPercentile /*Gets all information and combines it with DurPercentile*/
            FROM  Durations
            ) A2
            WHERE A1.DurPercentile = A2.DurPercentile)
            GROUP BY Hour, AverageDuration
            ORDER BY Counts desc"""
    return f"""WITH Durations AS (SELECT AID,StartDate,24 *60* extract(day FROM ENDDATE - STARTDATE) + 60*extract(hour from ENDDATE - STARTDATE) + extract(minute from ENDDATE - STARTDATE) as Duration
            FROM JPalavec.Accident)
            SELECT Count(*) as Counts, Hour, AverageDuration /*Format in correct form for Python heatmap*/
            FROM
            (SELECT EXTRACT(HOUR FROM StartDate) as Hour, AverageDuration 
            FROM
            (SELECT AVG(Duration) as AverageDuration, DurPercentile   /*Gets average duration of each DurPercentile*/
            FROM
            (SELECT Duration, NTILE(10) OVER (ORDER BY Duration) AS DurPercentile 
            FROM Durations
            )GROUP BY DurPercentile) A1,
            (SELECT AID,StartDate,Duration, NTILE(10) OVER (ORDER BY Duration) AS DurPercentile /*Gets all information and combines it with DurPercentile*/
            FROM  Durations
            ) A2
            WHERE A1.DurPercentile = A2.DurPercentile)
            GROUP BY Hour, AverageDuration
            ORDER BY Counts desc"""

def accidentsPopDensityGraph(state='All'):
    #Returns accidentCount, and PopDensity, could add County,state as labels. Graph as scatterplot
    print(state)
    if state != 'All':
        return f"""SELECT AccidentCount, C.state, C.county, C.Pop2018 / C.LandArea as PopDensity
            FROM(
            SELECT Count(*) as AccidentCount, C.county, C.state
            FROM JPalavec.Accident A
            JOIN JPalavec.County C ON A.county = C.county AND A.state = c.state
            WHERE C.county != 'All'
            GROUP BY C.county, C.state) AC,
            JPalavec.County C
            WHERE C.state = AC.state AND C.county = AC.county AND C.county != 'All' AND AC.state = '{state}'
            ORDER BY AccidentCount desc"""
    return f"""SELECT AccidentCount, C.state, C.county, C.Pop2018 / C.LandArea as PopDensity
            FROM(
            SELECT Count(*) as AccidentCount, C.county, C.state
            FROM JPalavec.Accident A
            JOIN JPalavec.County C ON A.county = C.county AND A.state = c.state
            WHERE C.county != 'All'
            GROUP BY C.county, C.state) AC,
            JPalavec.County C
            WHERE C.state = AC.state AND C.county = AC.county AND C.county != 'All'
            ORDER BY AccidentCount desc"""

def worstCountiesToLive(accidentPercentile='80'):
    return f"""SELECT fips, NVL(X.Damage,0) as DAMAGE, X.County, X.State
            FROM(
            SELECT A.County, A.State, Sum(DamageProperty+DamageCrops) as Damage FROM
            (
            SELECT AccidentCount, County, State, NTILE(100) Over (ORDER BY AccidentCount asc) as Percentile
            FROM
            (SELECT COUNT(*) as AccidentCount, County, State
            FROM JPalavec.Accident
            GROUP BY County, State)
            ) A
            LEFT JOIN JPalavec.Storm S ON S.county = A.county and S.state = A.state
            WHERE Percentile > '{accidentPercentile}'
            GROUP BY A.County, A.State
            ORDER BY Damage desc) X
            JOIN JPalavec.county C ON X.county = C.county AND X.state = C.state
            ORDER BY X.Damage desc"""


def accidentsFips():
    #Map all accidents in US by county
    return """
            SELECT c2.fips,count, count/(POP2018) as CountPC, c2.County, c2.STName, AvTemp
            FROM
            (
            SELECT fips, count(*) as count, AVG(Temperature) as AvTemp
            FROM JPALAVEC.accident a, JPALAVEC.county c
            WHERE a.county = c.county AND a.state = c.state 
            GROUP BY c.fips) c1,
            JPalavec.county c2
            WHERE c1.fips = c2.fips
        """

def accidentDurationState():
    #Map accident durations by state across US
    return """
        SELECT c1.AvDur, c2.STName, c2.state
        FROM(
        SELECT AVG(24 *60* extract(day FROM ENDDATE - STARTDATE) + 60*extract(hour from ENDDATE - STARTDATE) + extract(minute from ENDDATE - STARTDATE)) as AvDur, a.state
        FROM JPalavec.accident a
        JOIN JPalavec.county c
        ON a.state = c.state
        GROUP BY a.state
        )c1, JPalavec.county c2
        WHERE c1.state = c2.state
    """

def accidentSeverityState():
    #Map accident durations by state across US
    return """
        SELECT c1.AvSev, c2.STName, c2.state
        FROM(
        SELECT AVG(Severity) as AvSev, a.state
        FROM JPalavec.accident a
        JOIN JPalavec.county c
        ON a.state = c.state
        GROUP BY a.state
        )c1, JPalavec.county c2
        WHERE c1.state = c2.state
    """


def hourWeekdayAccident():
    return """
        SELECT Count(*) as COUNTS, Hour, Day, indexDay
        FROM
        (
        SELECT EXTRACT(HOUR FROM StartDate) as Hour,TO_CHAR(STARTDATE, 'fmDay') as Day,TO_CHAR(STARTDATE, 'D') indexDay
        FROM JPalavec.Accident
        )
        GROUP BY Hour, Day, indexDay
        ORDER BY indexDay asc
    """

def stormAccidentsVsExpectedAccidents(minutes = 60):
    return f"""
    SELECT SUM(ADS) as AccidentsDuringStorms, Sum(ExpectedAccidents) as ExpectedAccidents
    FROM(
    SELECT ADS, ACOUNT *( SCOUNT * {minutes}) / (26280 * 60) as ExpectedAccidents
    FROM
    (SELECT COUNT(*) as acount, County, State
    FROM Jpalavec.accident
    GROUP BY County, State) AC,
    (SELECT Count(*) as scount, County, State
    FROM JPalavec.storm
    GROUP BY County, State) SC,
    (SELECT Count(*) as ADS, A.County, A.State 
    FROM JPalavec.accident A
    JOIN JPalavec.Storm S ON A.county = s.county AND a.state = s.state
    WHERE (A.startdate > S.begindate AND A.startdate < S.begindate + interval '{minutes}' minute)
    OR (A.enddate > S.begindate AND A.enddate < S.begindate + interval '{minutes}' minute)
    GROUP BY A.county, A.state
    ) ADS
    WHERE ADS.county = SC.county AND ADS.state = SC.state AND ADS.state = AC.state AND ADS.county = AC.county)
    """