\echo

drop database cn;
create database cn;

\c cn;

drop table train;

create table train(
 train_id integer,
 train_name varchar(30),
 seats_total integer,
 seats_avail integer,
 from_place varchar(30),
 to_place varchar(30),
 dep_time time,
 arr_time time,
 no_of_stops integer,
 cost integer,
 waiting integer,
 tatkal_limit integer
);

create table customer(
 username varchar(30), /*username is ID*/
 passwd varchar(30),
 train_id_got integer,
 train_id_waiting integer
);
/*add a train_id to both so we know which train is being booked. or just add train name to customer*/

/*the third variable, seats_avail is small (1,2,3) so that we can demonstrate it with a couple of clients. waiting initialized to 0 for all. we will increment waiting if someone asks for a seat and it is full.*/
insert into train values(1,'Shatabdi Express',1280,2,'Delhi','Bombay','00:00','23:30',5,5000,0,20);
insert into train values(2,'Karnataka Express',990,1,'Bangalore','Chennai','05:00','11:00',6,4000,0,8);
insert into train values(3,'Delhi Express',1080,3,'Bangalore','Delhi','06:00','12:00',7,8000,0,18);
insert into train values(4,'Bangalore Express',1000,2,'Bangalore','Hyderabad','07:00','13:00',8,3000,0,20);
insert into train values(5,'Thomas the Tank Engine',980,1,'Kolkata','Srinagar','08:00','14:00',9,6000,0,25);
insert into train values(6,'PES Express',900,3,'Hosakerehalli','Hosakerehalli Petrol Bunk','09:00','15:00',8,500,0,18);
insert into train values(7,'Rajdhani Express',950,2,'Ahmedabad','Delhi','10:00','16:00',7,3000,0,21);
insert into train values(8,'Goa Express',1100,1,'Panaji','Bhopal','11:00','17:00',6,4000,0,10);

