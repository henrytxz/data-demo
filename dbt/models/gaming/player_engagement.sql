-- Note: to demonstrate dbt, I really could have picked a simpler query.
-- But this is also to show that I know SQL :) so picked a non-trivial SQL query.
-- This comes from https://leetcode.com/problems/game-play-analysis-iv/
-- Write an SQL query to report the fraction of players that logged in again on the day after the day
-- they first logged in, rounded to 2 decimal places.

SELECT
    ROUND(COUNT(t2.player_id)/COUNT(t1.player_id), 2) AS fraction
FROM
    (SELECT player_id, MIN(event_date) AS first_login FROM {{ ref('audit_game_play_activity') }} GROUP BY player_id) t1
LEFT JOIN {{ ref('audit_game_play_activity') }} t2
    ON t1.player_id = t2.player_id AND t1.first_login = t2.event_date - 1