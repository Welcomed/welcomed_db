drop table if exists hospitals;
drop table if exists doctors;
drop table if exists mentalhealth;
drop table if exists realestate;

create table hospitals (
  id integer primary key autoincrement,
  name text not null,
  latitude decimal not null,
  longitude decimal not null,
  address text not null
);
create table doctors (
  id integer primary key autoincrement,
  name text not null,
  latitude decimal not null,
  longitude decimal not null,
  address text not null
);
create table mentalhealth (
  id integer primary key autoincrement,
  name text not null,
  latitude decimal not null,
  longitude decimal not null,
  address text not null
);
create table realestate (
  id integer primary key autoincrement,
  name text not null,
  latitude decimal not null,
  longitude decimal not null,
  address text not null
);
