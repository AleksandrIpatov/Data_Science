with anapa_winter_flights as -- полеты из Анапы зимой 2017 года (январь, февраль, декабрь)
    (
        select
            *
        from
            dst_project.flights f
        where
            f.departure_airport = 'AAQ'
            and (date_trunc('month', f.scheduled_departure) in ('2017-01-01','2017-02-01', '2017-12-01'))
            and f.status != 'Cancelled'
    )
select
    distinct a.flight_id, -- номер рейса
    ap.city arrival_city, -- город назначения
    a.scheduled_departure::date date_departure_planed,
    count(tf.amount) sold_tickets, -- число проданных билетов
    sum(tf.amount) money_sold_tickets, -- сумма денег с проданных билетов
    extract (isodow from a.scheduled_departure) day_of_week, -- день недели (1 - пн, 7 - вс)
    date_part('hour', (a.actual_arrival::timestamp - a.actual_departure::timestamp)) * 60 + 
    date_part('minute', (a.actual_arrival::timestamp - a.actual_departure::timestamp)) flight_minutes_fact, -- полет в минутах
    date_part('hour', (a.actual_departure::timestamp - a.scheduled_departure::timestamp)) * 60 +
    date_part('minute', (a.actual_departure::timestamp - a.scheduled_departure::timestamp)) departure_delay, -- задержка вылета в минутах
    ac.model aircraft_model -- модель самолета
from
    anapa_winter_flights a
        left join dst_project.ticket_flights tf on a.flight_id = tf.flight_id
        left join dst_project.airports ap on a.arrival_airport = ap.airport_code
        left join dst_project.aircrafts ac on a.aircraft_code = ac.aircraft_code
group by 
    1,2,3,6,7,8,9
order by 
    3
