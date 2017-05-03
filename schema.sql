drop table if exists devices;
drop table if exists utilizacion;
drop table if exists interfaces;
drop table if exists category;


create table devices (
  device text not null primary key,
  ipAddress text not null,
  site text not null
);

create table utilizacion (
  device text not null,
  category text not null,
  interface integer,
  peakUtilization integer,
  kpi boolean
);

create table interfaces (
  device text not null,
  category text not null,
  FoC integer,
  current integer,
  lpu integer,
  capexLPU integer 
);

create table category (
  device text not null,
  capexCat money
);
