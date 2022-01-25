%function [V_phase_OPENDSS] = OPENDSS_interface_pqinj_three_phase_dynamic(t,load_var,Data,p_inj,q_inj)
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here
function[V_phase_OPENDSS] = pqinj_three_phase_static(Data,load_var,q_inj)
[DSSStartOK, DSSObj, DSSText] = DSSStartup;

if DSSStartOK

DSSObj.AllowForms = false;
DSSText.Command = 'Set DataPath =C:\Users\teghtesa\PycharmProjects\Volt\envs\power\ieee123_all_control';
DSSText.Command = 'Compile IEEE123Master.dss';   
 %lm=Data.load_var{t,2};
 lm=load_var;
% lm=0.8;
DSSText.Command=['set mode =snap loadmult=' num2str(lm)];
% fileID0=fopen('MyFile0.txt','w');
% fprintf(fileID0,'set mode=snap loadmult = %d',lm);
% formatSpec = '%c';
% fileID0_0 = fopen('MyFile0.txt','r');
% loadmult = fscanf(fileID0_0,formatSpec);
% DSSText.Command = loadmult;
% fclose(fileID0);
% fclose(fileID0_0);



% But in OPENDSS
% Opendss node sequence
% 150,149,1,2,3,7,4,5,6,8,12,9,13,14,34,18,11,10,15,16,17,19,21,20,22,23,24,25,26,28,27,31,33,29,30,250,32,35,36,40,37,38,39,41,42,43,44,45,47,46,49,50,51,151,52,53,54,55,57,56,58,60,
% 59,61,62,63,64,65,66,67,68,72,97,69,70,71,73,76,74,75,77,86,78,79,80,81,82,84,83,85,87,88,89,90,91,92,93,94,95,96,98,99,100,450,197,101,102,105,103,104,106,108,109,300,110,111,112,113,114,135,152,160,610]

%q_inj is the amount of reactive power that neesds to be injected by the
%generators
% p_inj=-p_inj(:,1).*(1000/lm);
q_inj(:,1)=-q_inj(:,1)*(1000/lm);
% p_inj(:,1)=p_inj(:,1).*1000;
% q_inj(:,1)=q_inj(:,1)*1000;
% 
% % For reactive power (1)
% DSSText.Command = ['New Load.DGQ149a phases=1 bus1=149.1 kV=2.4  Model=1 kw =0  kvar=' num2str(q_inj(1,1))]  ;
% DSSText.Command = ['New Load.DGQ149b phases=1 bus1=149.2 kV=2.4  Model=1 kw =0  kvar='  num2str(q_inj(2,1))]  ;
% DSSText.Command = ['New Load.DGQ149c phases=1 bus1=149.3 kV=2.4  Model=1 kw =0  kvar=' num2str(q_inj(3,1))]  ;
%(2)
DSSText.Command = ['New Load.DGQ1a phases=1 bus1=1.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(1,1))]  ;
DSSText.Command = ['New Load.DGQ1b phases=1 bus1=1.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(2,1))]  ;
DSSText.Command = ['New Load.DGQ1c phases=1 bus1=1.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(3,1))]  ;
% (3)
DSSText.Command = ['New Load.DGQ2b phases=1 bus1=2.2 kV=2.4 Model=1 kw =0 kvar=' num2str(q_inj(4,1))]  ;
%(4)
DSSText.Command = ['New Load.DGQ3c phases=1 bus1=3.3 kV=2.4 Model=1 kw =0 kvar=' num2str(q_inj(5,1))]  ;
%(5)
DSSText.Command = ['New Load.DGQ4c phases=1 bus1=4.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(6,1))]  ;
%(6)
DSSText.Command = ['New Load.DGQ5c phases=1 bus1=5.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(7,1))]  ;
%(7)
DSSText.Command = ['New Load.DGQ6c phases=1 bus1=6.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(8,1))]  ;
%(8)
DSSText.Command = ['New Load.DGQ7a phases=1 bus1=7.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(9,1))]  ;
DSSText.Command = ['New Load.DGQ7b phases=1 bus1=7.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(10,1))]  ;
DSSText.Command = ['New Load.DGQ7c phases=1 bus1=7.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(11,1))]  ;

% (9)
DSSText.Command = ['New Load.DGQ8a phases=1 bus1=8.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(12,1))]  ;
DSSText.Command = ['New Load.DGQ8b phases=1 bus1=8.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(13,1))]  ;
DSSText.Command = ['New Load.DGQ8c phases=1 bus1=8.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(14,1))]  ;
%(10)
DSSText.Command = ['New Load.DGQ9a phases=1 bus1=9.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(15,1))]  ;
%(11)
DSSText.Command = ['New Load.DGQ10a phases=1 bus1=10.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(16,1))]  ;
%(12)
DSSText.Command = ['New Load.DGQ11a phases=1 bus1=11.1 kV=2.4 Model=1 kw =0 kvar=' num2str(q_inj(17,1))]  ;

%(13)
DSSText.Command = ['New Load.DGQ12b phases=1 bus1=12.2 kV=2.4  Model=1 kw =0  kvar=' num2str(q_inj(18,1))]  ;

%(14)
DSSText.Command = ['New Load.DGQ13a phases=1 bus1=13.1 kV=2.4 Model=1 kw =0  kvar=' num2str(q_inj(19,1))]  ;
DSSText.Command = ['New Load.DGQ13b phases=1 bus1=13.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(20,1))]  ;
DSSText.Command = ['New Load.DGQ13c phases=1 bus1=13.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(21,1))]  ;
%(15)
DSSText.Command = ['New Load.DGQ14a phases=1 bus1=14.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(22,1))]  ;
%(16)
DSSText.Command = ['New Load.DGQ15c phases=1 bus1=15.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(23,1))]  ;
%(17)
DSSText.Command = ['New Load.DGQ16c phases=1 bus1=16.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(24,1))]  ;
%(18)
DSSText.Command = ['New Load.DGQ17c phases=1 bus1=17.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(25,1))]  ;

%(19)
DSSText.Command = ['New Load.DGQ18a phases=1 bus1=18.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(26,1))]  ;
DSSText.Command = ['New Load.DGQ18b phases=1 bus1=18.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(27,1))]  ;
DSSText.Command = ['New Load.DGQ18c phases=1 bus1=18.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(28,1))]  ;

%(20)
DSSText.Command = ['New Load.DGQ19a phases=1 bus1=19.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(29,1))]  ;

%(21)
DSSText.Command = ['New Load.DGQ20a phases=1 bus1=20.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(30,1))]  ;
%(22)
DSSText.Command = ['New Load.DGQ21a phases=1 bus1=21.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(31,1))]  ;
DSSText.Command = ['New Load.DGQ21b phases=1 bus1=21.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(32,1))]  ;
DSSText.Command = ['New Load.DGQ21c phases=1 bus1=21.3 kV=2.4  Model=1  kw =0 kvar=' num2str(q_inj(33,1))]  ;
%(23)
DSSText.Command = ['New Load.DGQ22b phases=1 bus1=22.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(34,1))]  ;
%(24)
DSSText.Command = ['New Load.DGQ23a phases=1 bus1=23.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(35,1))]  ;
DSSText.Command = ['New Load.DGQ23b phases=1 bus1=23.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(36,1))]  ;
DSSText.Command = ['New Load.DGQ23c phases=1 bus1=23.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(37,1))]  ;
%(25)
DSSText.Command = ['New Load.DGQ24c phases=1 bus1=24.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(38,1))]  ;
%(26)
DSSText.Command = ['New Load.DGQ25a phases=1 bus1=25.1 kV=2.4 Model=1  kw =0 kvar=' num2str(q_inj(39,1))]  ;
DSSText.Command = ['New Load.DGQ25b phases=1 bus1=25.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(40,1))]  ;
DSSText.Command = ['New Load.DGQ25c phases=1 bus1=25.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(41,1))]  ;
%(27)
DSSText.Command = ['New Load.DGQ26a phases=1 bus1=26.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(42,1))]  ;
DSSText.Command = ['New Load.DGQ26c phases=1 bus1=26.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(43,1))]  ;

%(28)
DSSText.Command = ['New Load.DGQ27a phases=1 bus1=27.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(44,1))]  ;
DSSText.Command = ['New Load.DGQ27c phases=1 bus1=27.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(45,1))]  ;
%(29)
DSSText.Command = ['New Load.DGQ28a phases=1 bus1=28.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(46,1))]  ;
DSSText.Command = ['New Load.DGQ28b phases=1 bus1=28.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(47,1))]  ;
DSSText.Command = ['New Load.DGQ28c phases=1 bus1=28.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(48,1))]  ;
%(30)
DSSText.Command = ['New Load.DGQ29a phases=1 bus1=29.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(49,1))]  ;
DSSText.Command = ['New Load.DGQ29b phases=1 bus1=29.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(50,1))]  ;
DSSText.Command = ['New Load.DGQ29c phases=1 bus1=29.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(51,1))]  ;
%(31)
DSSText.Command = ['New Load.DGQ30a phases=1 bus1=30.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(52,1))]  ;
DSSText.Command = ['New Load.DGQ30b phases=1 bus1=30.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(53,1))]  ;
DSSText.Command = ['New Load.DGQ30c phases=1 bus1=30.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(54,1))]  ;
%(32)
DSSText.Command = ['New Load.DGQ250a phases=1 bus1=250.1 kV=2.4 Model=1  kw =0 kvar=' num2str(q_inj(55,1))]  ;
DSSText.Command = ['New Load.DGQ250b phases=1 bus1=250.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(56,1))]  ;
DSSText.Command = ['New Load.DGQ250c phases=1 bus1=250.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(57,1))]  ;
%(33)
DSSText.Command = ['New Load.DGQ31c phases=1 bus1=31.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(58,1))]  ;
%(34)
DSSText.Command = ['New Load.DGQ32c phases=1 bus1=32.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(59,1))]  ;

%(35)
DSSText.Command = ['New Load.DGQ33a phases=1 bus1=33.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(60,1))]  ;
%(36)
DSSText.Command = ['New Load.DGQ34c phases=1 bus1=34.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(61,1))]  ;

%(38)
DSSText.Command = ['New Load.DGQ35a phases=1 bus1=35.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(62,1))]  ;
DSSText.Command = ['New Load.DGQ35b phases=1 bus1=35.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(63,1))]  ;
DSSText.Command = ['New Load.DGQ35c phases=1 bus1=35.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(64,1))]  ;
%(39)
DSSText.Command = ['New Load.DGQ36a phases=1 bus1=36.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(65,1))]  ;
DSSText.Command = ['New Load.DGQ36b phases=1 bus1=36.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(66,1))]  ;
%(40)
DSSText.Command = ['New Load.DGQ37a phases=1 bus1=37.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(67,1))]  ;
%(41)
DSSText.Command = ['New Load.DGQ38b phases=1 bus1=38.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(68,1))]  ;
%(42)
DSSText.Command = ['New Load.DGQ39b phases=1 bus1=39.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(69,1))]  ;
%(43)
DSSText.Command = ['New Load.DGQ40a phases=1 bus1=40.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(70,1))]  ;
DSSText.Command = ['New Load.DGQ40b phases=1 bus1=40.2 kV=2.4  Model=1 kw =0  kvar=' num2str(q_inj(71,1))]  ;
DSSText.Command = ['New Load.DGQ40c phases=1 bus1=40.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(72,1))]  ;

%(44)
DSSText.Command = ['New Load.DGQ41c phases=1 bus1=41.3 kV=2.4  Model=1 kw =0  kvar=' num2str(q_inj(73,1))]  ;
%(45)
DSSText.Command = ['New Load.DGQ42a phases=1 bus1=42.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(74,1))]  ;
DSSText.Command = ['New Load.DGQ42b phases=1 bus1=42.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(75,1))]  ;
DSSText.Command = ['New Load.DGQ42c phases=1 bus1=42.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(76,1))]  ;
%(46)
DSSText.Command = ['New Load.DGQ43b phases=1 bus1=43.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(77,1))]  ;
%(47)
DSSText.Command = ['New Load.DGQ44a phases=1 bus1=44.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(78,1))]  ;
DSSText.Command = ['New Load.DGQ44b phases=1 bus1=44.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(79,1))]  ;
DSSText.Command = ['New Load.DGQ44c phases=1 bus1=44.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(80,1))]  ;
%(48)
DSSText.Command = ['New Load.DGQ45a phases=1 bus1=45.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(81,1))]  ;
%(49)
DSSText.Command = ['New Load.DGQ46a phases=1 bus1=46.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(82,1))]  ;
%(50)
DSSText.Command = ['New Load.DGQ47a phases=1 bus1=47.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(83,1))]  ;
DSSText.Command = ['New Load.DGQ47b phases=1 bus1=47.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(84,1))]  ;
DSSText.Command = ['New Load.DGQ47c phases=1 bus1=47.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(85,1))]  ;

%(51)
DSSText.Command = ['New Load.DGQ48a phases=1 bus1=48.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(86,1))]  ;
DSSText.Command = ['New Load.DGQ48b phases=1 bus1=48.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(87,1))]  ;
DSSText.Command = ['New Load.DGQ48c phases=1 bus1=48.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(88,1))]  ;
%(52)
DSSText.Command = ['New Load.DGQ49a phases=1 bus1=49.1 kV=2.4  Model=1 kw =0  kvar=' num2str(q_inj(89,1))]  ;
DSSText.Command = ['New Load.DGQ49b phases=1 bus1=49.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(90,1))]  ;
DSSText.Command = ['New Load.DGQ49c phases=1 bus1=49.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(91,1))]  ;
%(53)
DSSText.Command = ['New Load.DGQ50a phases=1 bus1=50.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(92,1))]  ;
DSSText.Command = ['New Load.DGQ50b phases=1 bus1=50.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(93,1))]  ;
DSSText.Command = ['New Load.DGQ50c phases=1 bus1=50.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(94,1))]  ;
%(54)
DSSText.Command = ['New Load.DGQ51a phases=1 bus1=51.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(95,1))]  ;
DSSText.Command = ['New Load.DGQ51b phases=1 bus1=51.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(96,1))]  ;
DSSText.Command = ['New Load.DGQ51c phases=1 bus1=51.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(97,1))]  ;
%(55)
DSSText.Command = ['New Load.DGQ151a phases=1 bus1=151.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(98,1))]  ;
DSSText.Command = ['New Load.DGQ151b phases=1 bus1=151.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(99,1))]  ;
DSSText.Command = ['New Load.DGQ151c phases=1 bus1=151.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(100,1))]  ;
% 

%(57)
DSSText.Command = ['New Load.DGQ52a phases=1 bus1=52.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(101,1))]  ;
DSSText.Command = ['New Load.DGQ52b phases=1 bus1=52.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(102,1))]  ;
DSSText.Command = ['New Load.DGQ52c phases=1 bus1=52.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(103,1))]  ;
%(58)
DSSText.Command = ['New Load.DGQ53a phases=1 bus1=53.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(104,1))]  ;
DSSText.Command = ['New Load.DGQ53b phases=1 bus1=53.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(105,1))]  ;
DSSText.Command = ['New Load.DGQ53c phases=1 bus1=53.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(106,1))]  ;
%(59)
DSSText.Command = ['New Load.DGQ54a phases=1 bus1=54.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(107,1))]  ;
DSSText.Command = ['New Load.DGQ54b phases=1 bus1=54.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(108,1))]  ;
DSSText.Command = ['New Load.DGQ54c phases=1 bus1=54.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(109,1))]  ;
%(60)
DSSText.Command = ['New Load.DGQ55a phases=1 bus1=55.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(110,1))]  ;
DSSText.Command = ['New Load.DGQ55b phases=1 bus1=55.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(111,1))]  ;
DSSText.Command = ['New Load.DGQ55c phases=1 bus1=55.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(112,1))]  ;
%(61)
DSSText.Command = ['New Load.DGQ56a phases=1 bus1=56.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(113,1))]  ;
DSSText.Command = ['New Load.DGQ56b phases=1 bus1=56.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(114,1))]  ;
DSSText.Command = ['New Load.DGQ56c phases=1 bus1=56.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(115,1))]  ;
%(62)
DSSText.Command = ['New Load.DGQ57a phases=1 bus1=57.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(116,1))]  ;
DSSText.Command = ['New Load.DGQ57b phases=1 bus1=57.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(117,1))]  ;
DSSText.Command = ['New Load.DGQ57c phases=1 bus1=57.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(118,1))]  ;

%(63)
DSSText.Command = ['New Load.DGQ58b phases=1 bus1=58.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(119,1))]  ;
%(64)
DSSText.Command = ['New Load.DGQ59b phases=1 bus1=59.2 kV=2.4 Model=1  kw =0 kvar=' num2str(q_inj(120,1))]  ;
%(65)
DSSText.Command = ['New Load.DGQ60a phases=1 bus1=60.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(121,1))]  ;
DSSText.Command = ['New Load.DGQ60b phases=1 bus1=60.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(122,1))]  ;
DSSText.Command = ['New Load.DGQ60c phases=1 bus1=60.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(123,1))]  ;
%(66)
DSSText.Command = ['New Load.DGQ61a phases=1 bus1=61.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(124,1))]  ;
DSSText.Command = ['New Load.DGQ61b phases=1 bus1=61.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(125,1))]  ;
DSSText.Command = ['New Load.DGQ61c phases=1 bus1=61.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(126,1))]  ;

DSSText.Command = ['New Load.DGQ62a phases=1 bus1=62.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(127,1))]  ;
DSSText.Command = ['New Load.DGQ62b phases=1 bus1=62.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(128,1))]  ;
DSSText.Command = ['New Load.DGQ62c phases=1 bus1=62.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(129,1))]  ;
%(69)
DSSText.Command = ['New Load.DGQ63a phases=1 bus1=63.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(130,1))]  ;
DSSText.Command = ['New Load.DGQ63b phases=1 bus1=63.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(131,1))]  ;
DSSText.Command = ['New Load.DGQ63c phases=1 bus1=63.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(132,1))]  ;
%(70)
DSSText.Command = ['New Load.DGQ64a phases=1 bus1=64.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(133,1))]  ;
DSSText.Command = ['New Load.DGQ64b phases=1 bus1=64.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(134,1))]  ;
DSSText.Command = ['New Load.DGQ64c phases=1 bus1=64.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(135,1))]  ;
%(71)
DSSText.Command = ['New Load.DGQ65a phases=1 bus1=65.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(136,1))]  ;
DSSText.Command = ['New Load.DGQ65b phases=1 bus1=65.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(137,1))]  ;
DSSText.Command = ['New Load.DGQ65c phases=1 bus1=65.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(138,1))]  ;
%(72)
DSSText.Command = ['New Load.DGQ66a phases=1 bus1=66.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(139,1))]  ;
DSSText.Command = ['New Load.DGQ66b phases=1 bus1=66.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(140,1))]  ;
DSSText.Command = ['New Load.DGQ66c phases=1 bus1=66.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(141,1))]  ;

%(74)
DSSText.Command = ['New Load.DGQ67a phases=1 bus1=67.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(142,1))]  ;
DSSText.Command = ['New Load.DGQ67b phases=1 bus1=67.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(143,1))]  ;
DSSText.Command = ['New Load.DGQ67c phases=1 bus1=67.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(144,1))]  ;
%(75)
DSSText.Command = ['New Load.DGQ68a phases=1 bus1=68.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(145,1))]  ;
%(76)
DSSText.Command = ['New Load.DGQ69a phases=1 bus1=69.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(146,1))]  ;
%(77)
DSSText.Command = ['New Load.DGQ70a phases=1 bus1=70.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(147,1))]  ;
%(78)
DSSText.Command = ['New Load.DGQ71a phases=1 bus1=71.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(148,1))]  ;
%(79)
DSSText.Command = ['New Load.DGQ72a phases=1 bus1=72.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(149,1))]  ;
DSSText.Command = ['New Load.DGQ72b phases=1 bus1=72.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(150,1))]  ;
DSSText.Command = ['New Load.DGQ72c phases=1 bus1=72.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(151,1))]  ;
%(80)
DSSText.Command = ['New Load.DGQ73c phases=1 bus1=73.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(152,1))]  ;
%(81)
DSSText.Command = ['New Load.DGQ74c phases=1 bus1=74.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(153,1))]  ;
%(82)
DSSText.Command = ['New Load.DGQ75c phases=1 bus1=75.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(154,1))]  ;
%(83)
DSSText.Command = ['New Load.DGQ76a phases=1 bus1=76.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(155,1))]  ;
DSSText.Command = ['New Load.DGQ76b phases=1 bus1=76.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(156,1))]  ;
DSSText.Command = ['New Load.DGQ76c phases=1 bus1=76.3 kV=2.4  Model=1 kw =0  kvar=' num2str(q_inj(157,1))]  ;
%(84)
DSSText.Command = ['New Load.DGQ77a phases=1 bus1=77.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(158,1))]  ;
DSSText.Command = ['New Load.DGQ77b phases=1 bus1=77.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(159,1))]  ;
DSSText.Command = ['New Load.DGQ77c phases=1 bus1=77.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(160,1))]  ;
%(85)
DSSText.Command = ['New Load.DGQ78a phases=1 bus1=78.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(161,1))]  ;
DSSText.Command = ['New Load.DGQ78b phases=1 bus1=78.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(162,1))]  ;
DSSText.Command = ['New Load.DGQ78c phases=1 bus1=78.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(163,1))]  ;
%(86)
DSSText.Command = ['New Load.DGQ79a phases=1 bus1=79.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(164,1))]  ;
DSSText.Command = ['New Load.DGQ79b phases=1 bus1=79.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(165,1))]  ;
DSSText.Command = ['New Load.DGQ79c phases=1 bus1=79.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(166,1))]  ;
%(87)
DSSText.Command = ['New Load.DGQ80a phases=1 bus1=80.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(167,1))]  ;
DSSText.Command = ['New Load.DGQ80b phases=1 bus1=80.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(168,1))]  ;
DSSText.Command = ['New Load.DGQ80c phases=1 bus1=80.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(169,1))]  ;
%(88)
DSSText.Command = ['New Load.DGQ81a phases=1 bus1=81.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(170,1))]  ;
DSSText.Command = ['New Load.DGQ81b phases=1 bus1=81.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(171,1))]  ;
DSSText.Command = ['New Load.DGQ81c phases=1 bus1=81.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(172,1))]  ;
%(89)
DSSText.Command = ['New Load.DGQ82a phases=1 bus1=82.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(173,1))]  ;
DSSText.Command = ['New Load.DGQ82b phases=1 bus1=82.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(174,1))]  ;
DSSText.Command = ['New Load.DGQ82c phases=1 bus1=82.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(175,1))]  ;
%(90)
DSSText.Command = ['New Load.DGQ83a phases=1 bus1=83.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(176,1))]  ;
DSSText.Command = ['New Load.DGQ83b phases=1 bus1=83.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(177,1))]  ;
DSSText.Command = ['New Load.DGQ83c phases=1 bus1=83.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(178,1))]  ;
%(91)
DSSText.Command = ['New Load.DGQ84c phases=1 bus1=84.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(179,1))]  ;
%(92)
DSSText.Command = ['New Load.DGQ85c phases=1 bus1=85.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(180,1))]  ;
%(93)
DSSText.Command = ['New Load.DGQ86a phases=1 bus1=86.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(181,1))]  ;
DSSText.Command = ['New Load.DGQ86b phases=1 bus1=86.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(182,1))]  ;
DSSText.Command = ['New Load.DGQ86c phases=1 bus1=86.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(183,1))]  ;
%(94)
DSSText.Command = ['New Load.DGQ87a phases=1 bus1=87.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(184,1))]  ;
DSSText.Command = ['New Load.DGQ87b phases=1 bus1=87.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(185,1))]  ;
DSSText.Command = ['New Load.DGQ87c phases=1 bus1=87.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(186,1))]  ;
%(95)
DSSText.Command = ['New Load.DGQ88a phases=1 bus1=88.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(187,1))]  ;
%(96)
DSSText.Command = ['New Load.DGQ89a phases=1 bus1=89.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(188,1))]  ;
DSSText.Command = ['New Load.DGQ89b phases=1 bus1=89.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(189,1))]  ;
DSSText.Command = ['New Load.DGQ89c phases=1 bus1=89.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(190,1))]  ;
%(97)
DSSText.Command = ['New Load.DGQ90b phases=1 bus1=90.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(191,1))]  ;
%(98)
DSSText.Command = ['New Load.DGQ91a phases=1 bus1=91.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(192,1))]  ;
DSSText.Command = ['New Load.DGQ91b phases=1 bus1=91.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(193,1))]  ;
DSSText.Command = ['New Load.DGQ91c phases=1 bus1=91.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(194,1))]  ;
%(99)
DSSText.Command = ['New Load.DGQ92c phases=1 bus1=92.3 kV=2.4  Model=1  kw =0 kvar=' num2str(q_inj(195,1))]  ;
%(100)
DSSText.Command = ['New Load.DGQ93a phases=1 bus1=93.1 kV=2.4 Model=1  kw =0 kvar=' num2str(q_inj(196,1))]  ;
DSSText.Command = ['New Load.DGQ93b phases=1 bus1=93.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(197,1))]  ;
DSSText.Command = ['New Load.DGQ93c phases=1 bus1=93.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(198,1))]  ;
%(101)
DSSText.Command = ['New Load.DGQ94a phases=1 bus1=94.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(199,1))]  ;
%(102)
DSSText.Command = ['New Load.DGQ95a phases=1 bus1=95.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(200,1))]  ;
DSSText.Command = ['New Load.DGQ95b phases=1 bus1=95.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(201,1))]  ;
DSSText.Command = ['New Load.DGQ95c phases=1 bus1=95.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(202,1))]  ;
%(103)
DSSText.Command = ['New Load.DGQ96b phases=1 bus1=96.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(203,1))]  ;
%(104)
DSSText.Command = ['New Load.DGQ97a phases=1 bus1=97.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(204,1))]  ;
DSSText.Command = ['New Load.DGQ97b phases=1 bus1=97.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(205,1))]  ;
DSSText.Command = ['New Load.DGQ97c phases=1 bus1=97.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(206,1))]  ;
%(105)
DSSText.Command = ['New Load.DGQ98a phases=1 bus1=98.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(207,1))]  ;
DSSText.Command = ['New Load.DGQ98b phases=1 bus1=98.2 kV=2.4 Model=1  kw =0 kvar=' num2str(q_inj(208,1))]  ;
DSSText.Command = ['New Load.DGQ98c phases=1 bus1=98.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(209,1))]  ;
%(106)
DSSText.Command = ['New Load.DGQ99a phases=1 bus1=99.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(210,1))]  ;
DSSText.Command = ['New Load.DGQ99b phases=1 bus1=99.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(211,1))]  ;
DSSText.Command = ['New Load.DGQ99c phases=1 bus1=99.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(212,1))]  ;
%(107)
DSSText.Command = ['New Load.DGQ100a phases=1 bus1=100.1 kV=2.4 Model=1  kw =0 kvar=' num2str(q_inj(213,1))]  ;
DSSText.Command = ['New Load.DGQ100b phases=1 bus1=100.2 kV=2.4 Model=1  kw =0 kvar=' num2str(q_inj(214,1))]  ;
DSSText.Command = ['New Load.DGQ100c phases=1 bus1=100.3 kV=2.4 Model=1  kw =0 kvar=' num2str(q_inj(215,1))]  ;
%(108)
DSSText.Command = ['New Load.DGQ450a phases=1 bus1=450.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(216,1))]  ;
DSSText.Command = ['New Load.DGQ450b phases=1 bus1=450.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(217,1))]  ;
DSSText.Command = ['New Load.DGQ450c phases=1 bus1=450.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(218,1))]  ;

%(110)
DSSText.Command = ['New Load.DGQ101a phases=1 bus1=101.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(219,1))]  ;
DSSText.Command = ['New Load.DGQ101b phases=1 bus1=101.2 kV=2.4  Model=1 kw =0  kvar=' num2str(q_inj(220,1))]  ;
DSSText.Command = ['New Load.DGQ101c phases=1 bus1=101.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(221,1))]  ;
%(111)
DSSText.Command = ['New Load.DGQ102c phases=1 bus1=102.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(222,1))]  ;
%(112)
DSSText.Command = ['New Load.DGQ103c phases=1 bus1=103.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(223,1))]  ;
%(113)
DSSText.Command = ['New Load.DGQ104c phases=1 bus1=104.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(224,1))]  ;
%(114)
DSSText.Command = ['New Load.DGQ105a phases=1 bus1=105.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(225,1))]  ;
DSSText.Command = ['New Load.DGQ105b phases=1 bus1=105.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(226,1))]  ;
DSSText.Command = ['New Load.DGQ105c phases=1 bus1=105.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(227,1))]  ;
%(115)
DSSText.Command = ['New Load.DGQ106b phases=1 bus1=106.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(228,1))]  ;
%(116)
DSSText.Command = ['New Load.DGQ107b phases=1 bus1=107.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(229,1))]  ;
%(117)
DSSText.Command = ['New Load.DGQ108a phases=1 bus1=108.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(230,1))]  ;
DSSText.Command = ['New Load.DGQ108b phases=1 bus1=108.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(231,1))]  ;
DSSText.Command = ['New Load.DGQ108c phases=1 bus1=108.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(232,1))]  ;
%(118)
DSSText.Command = ['New Load.DGQ109a phases=1 bus1=109.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(233,1))]  ;
%(119)
DSSText.Command = ['New Load.DGQ110a phases=1 bus1=110.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(234,1))]  ;
%(120)
DSSText.Command = ['New Load.DGQ111a phases=1 bus1=111.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(235,1))]  ;
%(121)
DSSText.Command = ['New Load.DGQ112a phases=1 bus1=112.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(236,1))]  ;
%(122)
DSSText.Command = ['New Load.DGQ113a phases=1 bus1=113.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(237,1))]  ;
%(123)
DSSText.Command = ['New Load.DGQ114a phases=1 bus1=114.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(238,1))]  ;

%(124)
DSSText.Command = ['New Load.DGQ300a phases=1 bus1=300.1 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(239,1))]  ;
DSSText.Command = ['New Load.DGQ300b phases=1 bus1=300.2 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(240,1))]  ;
DSSText.Command = ['New Load.DGQ300c phases=1 bus1=300.3 kV=2.4  Model=1 kw =0 kvar=' num2str(q_inj(241,1))]  ;

% % 
% % % % For active power (1)
% % DSSText.Command = ['New Load.DGP149a phases=1 bus1=149.1 kV=2.4 Model=1  pf=1 Kw=  ' num2str(p_inj(1,1))]  ;
% % DSSText.Command = ['New Load.DGP149b phases=1 bus1=149.2 kV=2.4  Model=1  pf=1  Kw=  ' num2str(p_inj(2,1))]  ;
% % DSSText.Command = ['New Load.DGP149c phases=1 bus1=149.3 kV=2.4  Model=1  pf=1  Kw=  ' num2str(p_inj(3,1))]  ;
% %(2)
% DSSText.Command = ['New Load.DGP1a phases=1 bus1=1.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(1,1))]  ;
% DSSText.Command = ['New Load.DGP1b phases=1 bus1=1.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(2,1))]  ;
% DSSText.Command = ['New Load.DGP1c phases=1 bus1=1.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(3,1))]  ;
% % (3)
% DSSText.Command = ['New Load.DGP2b phases=1 bus1=2.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(4,1))]  ;
% %(4)
% DSSText.Command = ['New Load.DGP3c phases=1 bus1=3.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(5,1))]  ;
% %(5)
% DSSText.Command = ['New Load.DGP4c phases=1 bus1=4.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(6,1))]  ;
% %(6)
% DSSText.Command = ['New Load.DGP5c phases=1 bus1=5.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(7,1))]  ;
% %(7)
% DSSText.Command = ['New Load.DGP6c phases=1 bus1=6.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(8,1))]  ;
% %(8)
% DSSText.Command = ['New Load.DGP7a phases=1 bus1=7.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(9,1))]  ;
% DSSText.Command = ['New Load.DGP7b phases=1 bus1=7.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(10,1))]  ;
% DSSText.Command = ['New Load.DGP7c phases=1 bus1=7.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(11,1))]  ;
% 
% % (9)
% DSSText.Command = ['New Load.DGP8a phases=1 bus1=8.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(12,1))]  ;
% DSSText.Command = ['New Load.DGP8b phases=1 bus1=8.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(13,1))]  ;
% DSSText.Command = ['New Load.DGP8c phases=1 bus1=8.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(14,1))]  ;
% %(10)
% DSSText.Command = ['New Load.DGP9a phases=1 bus1=9.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(15,1))]  ;
% %(11)
% DSSText.Command = ['New Load.DGP10a phases=1 bus1=10.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(16,1))]  ;
% %(12)
% DSSText.Command = ['New Load.DGP11a phases=1 bus1=11.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(17,1))]  ;
% 
% %(13)
% DSSText.Command = ['New Load.DGP12b phases=1 bus1=12.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(18,1))]  ;
% 
% %(14)
% DSSText.Command = ['New Load.DGP13a phases=1 bus1=13.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(19,1))]  ;
% DSSText.Command = ['New Load.DGP13b phases=1 bus1=13.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(20,1))]  ;
% DSSText.Command = ['New Load.DGP13c phases=1 bus1=13.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(21,1))]  ;
% %(15)
% DSSText.Command = ['New Load.DGP14a phases=1 bus1=14.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(22,1))]  ;
% %(16)
% DSSText.Command = ['New Load.DGP15c phases=1 bus1=15.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(23,1))]  ;
% %(17)
% DSSText.Command = ['New Load.DGP16c phases=1 bus1=16.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(24,1))]  ;
% %(18)
% DSSText.Command = ['New Load.DGP17c phases=1 bus1=17.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(25,1))]  ;
% 
% %(19)
% DSSText.Command = ['New Load.DGP18a phases=1 bus1=18.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(26,1))]  ;
% DSSText.Command = ['New Load.DGP18b phases=1 bus1=18.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(27,1))]  ;
% DSSText.Command = ['New Load.DGP18c phases=1 bus1=18.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(28,1))]  ;
% 
% %(20)
% DSSText.Command = ['New Load.DGP19a phases=1 bus1=19.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(29,1))]  ;
% 
% %(21)
% DSSText.Command = ['New Load.DGP20a phases=1 bus1=20.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(30,1))]  ;
% %(22)
% DSSText.Command = ['New Load.DGP21a phases=1 bus1=21.1 kV=2.4 Model=1  pf=1  Kw=' num2str(p_inj(31,1))]  ;
% DSSText.Command = ['New Load.DGP21b phases=1 bus1=21.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(32,1))]  ;
% DSSText.Command = ['New Load.DGP21c phases=1 bus1=21.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(33,1))]  ;
% %(23)
% DSSText.Command = ['New Load.DGP22b phases=1 bus1=22.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(34,1))]  ;
% %(24)
% DSSText.Command = ['New Load.DGP23a phases=1 bus1=23.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(35,1))]  ;
% DSSText.Command = ['New Load.DGP23b phases=1 bus1=23.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(36,1))]  ;
% DSSText.Command = ['New Load.DGP23c phases=1 bus1=23.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(37,1))]  ;
% %(25)
% DSSText.Command = ['New Load.DGP24c phases=1 bus1=24.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(38,1))]  ;
% %(26)
% DSSText.Command = ['New Load.DGP25a phases=1 bus1=25.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(39,1))]  ;
% DSSText.Command = ['New Load.DGP25b phases=1 bus1=25.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(40,1))]  ;
% DSSText.Command = ['New Load.DGP25c phases=1 bus1=25.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(41,1))]  ;
% %(27)
% DSSText.Command = ['New Load.DGP26a phases=1 bus1=26.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(42,1))]  ;
% DSSText.Command = ['New Load.DGP26c phases=1 bus1=26.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(43,1))]  ;
% 
% %(28)
% DSSText.Command = ['New Load.DGP27a phases=1 bus1=27.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(44,1))]  ;
% DSSText.Command = ['New Load.DGP27c phases=1 bus1=27.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(45,1))]  ;
% %(29)
% DSSText.Command = ['New Load.DGP28a phases=1 bus1=28.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(46,1))]  ;
% DSSText.Command = ['New Load.DGP28b phases=1 bus1=28.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(47,1))]  ;
% DSSText.Command = ['New Load.DGP28c phases=1 bus1=28.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(48,1))]  ;
% %(30)
% DSSText.Command = ['New Load.DGP29a phases=1 bus1=29.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(49,1))]  ;
% DSSText.Command = ['New Load.DGP29b phases=1 bus1=29.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(50,1))]  ;
% DSSText.Command = ['New Load.DGP29c phases=1 bus1=29.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(51,1))]  ;
% %(31)
% DSSText.Command = ['New Load.DGP30a phases=1 bus1=30.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(52,1))]  ;
% DSSText.Command = ['New Load.DGP30b phases=1 bus1=30.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(53,1))]  ;
% DSSText.Command = ['New Load.DGP30c phases=1 bus1=30.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(54,1))]  ;
% %(32)
% DSSText.Command = ['New Load.DGP250a phases=1 bus1=250.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(55,1))]  ;
% DSSText.Command = ['New Load.DGP250b phases=1 bus1=250.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(56,1))]  ;
% DSSText.Command = ['New Load.DGP250c phases=1 bus1=250.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(57,1))]  ;
% %(33)
% DSSText.Command = ['New Load.DGP31c phases=1 bus1=31.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(58,1))]  ;
% %(34)
% DSSText.Command = ['New Load.DGP32c phases=1 bus1=32.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(59,1))]  ;
% 
% %(35)
% DSSText.Command = ['New Load.DGP33a phases=1 bus1=33.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(60,1))]  ;
% %(36)
% DSSText.Command = ['New Load.DGP34c phases=1 bus1=34.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(61,1))]  ;
% 
% %(38)
% DSSText.Command = ['New Load.DGP35a phases=1 bus1=35.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(62,1))]  ;
% DSSText.Command = ['New Load.DGP35b phases=1 bus1=35.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(63,1))]  ;
% DSSText.Command = ['New Load.DGP35c phases=1 bus1=35.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(64,1))]  ;
% %(39)
% DSSText.Command = ['New Load.DGP36a phases=1 bus1=36.1 kV=2.4 Model=1  pf=1  Kw=' num2str(p_inj(65,1))]  ;
% DSSText.Command = ['New Load.DGP36b phases=1 bus1=36.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(66,1))]  ;
% %(40)
% DSSText.Command = ['New Load.DGP37a phases=1 bus1=37.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(67,1))]  ;
% %(41)
% DSSText.Command = ['New Load.DGP38b phases=1 bus1=38.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(68,1))]  ;
% %(42)
% DSSText.Command = ['New Load.DGP39b phases=1 bus1=39.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(69,1))]  ;
% %(43)
% DSSText.Command = ['New Load.DGP40a phases=1 bus1=40.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(70,1))]  ;
% DSSText.Command = ['New Load.DGP40b phases=1 bus1=40.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(71,1))]  ;
% DSSText.Command = ['New Load.DGP40c phases=1 bus1=40.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(72,1))]  ;
% 
% %(44)
% DSSText.Command = ['New Load.DGP41c phases=1 bus1=41.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(73,1))]  ;
% %(45)
% DSSText.Command = ['New Load.DGP42a phases=1 bus1=42.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(74,1))]  ;
% DSSText.Command = ['New Load.DGP42b phases=1 bus1=42.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(75,1))]  ;
% DSSText.Command = ['New Load.DGP42c phases=1 bus1=42.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(76,1))]  ;
% %(46)
% DSSText.Command = ['New Load.DGP43b phases=1 bus1=43.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(77,1))]  ;
% %(47)
% DSSText.Command = ['New Load.DGP44a phases=1 bus1=44.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(78,1))]  ;
% DSSText.Command = ['New Load.DGP44b phases=1 bus1=44.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(79,1))]  ;
% DSSText.Command = ['New Load.DGP44c phases=1 bus1=44.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(80,1))]  ;
% %(48)
% DSSText.Command = ['New Load.DGP45a phases=1 bus1=45.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(81,1))]  ;
% %(49)
% DSSText.Command = ['New Load.DGP46a phases=1 bus1=46.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(82,1))]  ;
% %(50)
% DSSText.Command = ['New Load.DGP47a phases=1 bus1=47.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(83,1))]  ;
% DSSText.Command = ['New Load.DGP47b phases=1 bus1=47.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(84,1))]  ;
% DSSText.Command = ['New Load.DGP47c phases=1 bus1=47.3 kV=2.4 Model=1  pf=1  Kw=' num2str(p_inj(85,1))]  ;
% % 
% % %(51)
% DSSText.Command = ['New Load.DGP48a phases=1 bus1=48.1 kV=2.4 Model=1  pf=1  Kw=' num2str(p_inj(86,1))]  ;
% DSSText.Command = ['New Load.DGP48b phases=1 bus1=48.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(87,1))]  ;
% DSSText.Command = ['New Load.DGP48c phases=1 bus1=48.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(88,1))]  ;
% %(52)
% DSSText.Command = ['New Load.DGP49a phases=1 bus1=49.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(89,1))]  ;
% DSSText.Command = ['New Load.DGP49b phases=1 bus1=49.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(90,1))]  ;
% DSSText.Command = ['New Load.DGP49c phases=1 bus1=49.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(91,1))]  ;
% %(53)
% DSSText.Command = ['New Load.DGP50a phases=1 bus1=50.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(92,1))]  ;
% DSSText.Command = ['New Load.DGP50b phases=1 bus1=50.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(93,1))]  ;
% DSSText.Command = ['New Load.DGP50c phases=1 bus1=50.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(94,1))]  ;
% %(54)
% DSSText.Command = ['New Load.DGP51a phases=1 bus1=51.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(95,1))]  ;
% DSSText.Command = ['New Load.DGP51b phases=1 bus1=51.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(96,1))]  ;
% DSSText.Command = ['New Load.DGP51c phases=1 bus1=51.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(97,1))]  ;
% %(55)
% DSSText.Command = ['New Load.DGP151a phases=1 bus1=151.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(98,1))]  ;
% DSSText.Command = ['New Load.DGP151b phases=1 bus1=151.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(99,1))]  ;
% DSSText.Command = ['New Load.DGP151c phases=1 bus1=151.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(100,1))]  ;
% 
% %(57)
% DSSText.Command = ['New Load.DGP52a phases=1 bus1=52.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(101,1))]  ;
% DSSText.Command = ['New Load.DGP52b phases=1 bus1=52.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(102,1))]  ;
% DSSText.Command = ['New Load.DGP52c phases=1 bus1=52.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(103,1))]  ;
% %(58)
% DSSText.Command = ['New Load.DGP53a phases=1 bus1=53.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(104,1))]  ;
% DSSText.Command = ['New Load.DGP53b phases=1 bus1=53.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(105,1))]  ;
% DSSText.Command = ['New Load.DGP53c phases=1 bus1=53.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(106,1))]  ;
% %(59)
% DSSText.Command = ['New Load.DGP54a phases=1 bus1=54.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(107,1))]  ;
% DSSText.Command = ['New Load.DGP54b phases=1 bus1=54.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(108,1))]  ;
% DSSText.Command = ['New Load.DGP54c phases=1 bus1=54.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(109,1))]  ;
% %(60)
% DSSText.Command = ['New Load.DGP55a phases=1 bus1=55.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(110,1))]  ;
% DSSText.Command = ['New Load.DGP55b phases=1 bus1=55.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(111,1))]  ;
% DSSText.Command = ['New Load.DGP55c phases=1 bus1=55.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(112,1))]  ;
% %(61)
% DSSText.Command = ['New Load.DGP56a phases=1 bus1=56.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(113,1))]  ;
% DSSText.Command = ['New Load.DGP56b phases=1 bus1=56.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(114,1))]  ;
% DSSText.Command = ['New Load.DGP56c phases=1 bus1=56.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(115,1))]  ;
% %(62)
% DSSText.Command = ['New Load.DGP57a phases=1 bus1=57.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(116,1))]  ;
% DSSText.Command = ['New Load.DGP57b phases=1 bus1=57.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(117,1))]  ;
% DSSText.Command = ['New Load.DGP57c phases=1 bus1=57.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(118,1))]  ;
% 
% %(63)
% DSSText.Command = ['New Load.DGP58b phases=1 bus1=58.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(119,1))]  ;
% %(64)
% DSSText.Command = ['New Load.DGP59b phases=1 bus1=59.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(120,1))]  ;
% %(65)
% DSSText.Command = ['New Load.DGP60a phases=1 bus1=60.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(121,1))]  ;
% DSSText.Command = ['New Load.DGP60b phases=1 bus1=60.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(122,1))]  ;
% DSSText.Command = ['New Load.DGP60c phases=1 bus1=60.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(123,1))]  ;
% %(66)
% DSSText.Command = ['New Load.DGP61a phases=1 bus1=61.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(124,1))]  ;
% DSSText.Command = ['New Load.DGP61b phases=1 bus1=61.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(125,1))]  ;
% DSSText.Command = ['New Load.DGP61c phases=1 bus1=61.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(126,1))]  ;
% 
% %(68)
% DSSText.Command = ['New Load.DGP62a phases=1 bus1=62.1 kV=2.4 Model=1  pf=1  Kw=' num2str(p_inj(127,1))]  ;
% DSSText.Command = ['New Load.DGP62b phases=1 bus1=62.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(128,1))]  ;
% DSSText.Command = ['New Load.DGP62c phases=1 bus1=62.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(129,1))]  ;
% %(69)
% DSSText.Command = ['New Load.DGP63a phases=1 bus1=63.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(130,1))]  ;
% DSSText.Command = ['New Load.DGP63b phases=1 bus1=63.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(131,1))]  ;
% DSSText.Command = ['New Load.DGP63c phases=1 bus1=63.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(132,1))]  ;
% %(70)
% DSSText.Command = ['New Load.DGP64a phases=1 bus1=64.1 kV=2.4 Model=1  pf=1  Kw=' num2str(p_inj(133,1))]  ;
% DSSText.Command = ['New Load.DGP64b phases=1 bus1=64.2 kV=2.4 Model=1  pf=1  Kw=' num2str(p_inj(134,1))]  ;
% DSSText.Command = ['New Load.DGP64c phases=1 bus1=64.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(135,1))]  ;
% %(71)
% DSSText.Command = ['New Load.DGP65a phases=1 bus1=65.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(136,1))]  ;
% DSSText.Command = ['New Load.DGP65b phases=1 bus1=65.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(137,1))]  ;
% DSSText.Command = ['New Load.DGP65c phases=1 bus1=65.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(138,1))]  ;
% %(72)
% DSSText.Command = ['New Load.DGP66a phases=1 bus1=66.1 kV=2.4 Model=1  pf=1  Kw=' num2str(p_inj(139,1))]  ;
% DSSText.Command = ['New Load.DGP66b phases=1 bus1=66.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(140,1))]  ;
% DSSText.Command = ['New Load.DGP66c phases=1 bus1=66.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(141,1))]  ;
% 
% %(74)
% DSSText.Command = ['New Load.DGP67a phases=1 bus1=67.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(142,1))]  ;
% DSSText.Command = ['New Load.DGP67b phases=1 bus1=67.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(143,1))]  ;
% DSSText.Command = ['New Load.DGP67c phases=1 bus1=67.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(144,1))]  ;
% %(75)
% DSSText.Command = ['New Load.DGP68a phases=1 bus1=68.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(145,1))]  ;
% % %(76)
% DSSText.Command = ['New Load.DGP69a phases=1 bus1=69.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(146,1))]  ;
% %(77)
% DSSText.Command = ['New Load.DGP70a phases=1 bus1=70.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(147,1))]  ;
% %(78)
% DSSText.Command = ['New Load.DGP71a phases=1 bus1=71.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(148,1))]  ;
% %(79)
% DSSText.Command = ['New Load.DGP72a phases=1 bus1=72.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(149,1))]  ;
% DSSText.Command = ['New Load.DGP72b phases=1 bus1=72.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(150,1))]  ;
% DSSText.Command = ['New Load.DGP72c phases=1 bus1=72.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(151,1))]  ;
% %(80)
% DSSText.Command = ['New Load.DGP73c phases=1 bus1=73.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(152,1))]  ;
% %(81)
% DSSText.Command = ['New Load.DGP74c phases=1 bus1=74.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(153,1))]  ;
% %(82)
% DSSText.Command = ['New Load.DGP75c phases=1 bus1=75.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(154,1))]  ;
% %(83)
% DSSText.Command = ['New Load.DGP76a phases=1 bus1=76.1 kV=2.4 Model=1  pf=1  Kw=' num2str(p_inj(155,1))]  ;
% DSSText.Command = ['New Load.DGP76b phases=1 bus1=76.2 kV=2.4 Model=1  pf=1  Kw=' num2str(p_inj(156,1))]  ;
% DSSText.Command = ['New Load.DGP76c phases=1 bus1=76.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(157,1))]  ;
% %(84)
% DSSText.Command = ['New Load.DGP77a phases=1 bus1=77.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(158,1))]  ;
% DSSText.Command = ['New Load.DGP77b phases=1 bus1=77.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(159,1))]  ;
% DSSText.Command = ['New Load.DGP77c phases=1 bus1=77.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(160,1))]  ;
% %(85)
% DSSText.Command = ['New Load.DGP78a phases=1 bus1=78.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(161,1))]  ;
% DSSText.Command = ['New Load.DGP78b phases=1 bus1=78.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(162,1))]  ;
% DSSText.Command = ['New Load.DGP78c phases=1 bus1=78.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(163,1))]  ;
% %(86)
% DSSText.Command = ['New Load.DGP79a phases=1 bus1=79.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(164,1))]  ;
% DSSText.Command = ['New Load.DGP79b phases=1 bus1=79.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(165,1))]  ;
% DSSText.Command = ['New Load.DGP79c phases=1 bus1=79.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(166,1))]  ;
% %(87)
% DSSText.Command = ['New Load.DGP80a phases=1 bus1=80.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(167,1))]  ;
% DSSText.Command = ['New Load.DGP80b phases=1 bus1=80.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(168,1))]  ;
% DSSText.Command = ['New Load.DGP80c phases=1 bus1=80.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(169,1))]  ;
% %(88)
% DSSText.Command = ['New Load.DGP81a phases=1 bus1=81.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(170,1))]  ;
% DSSText.Command = ['New Load.DGP81b phases=1 bus1=81.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(171,1))]  ;
% DSSText.Command = ['New Load.DGP81c phases=1 bus1=81.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(172,1))]  ;
% %(89)
% DSSText.Command = ['New Load.DGP82a phases=1 bus1=82.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(173,1))]  ;
% DSSText.Command = ['New Load.DGP82b phases=1 bus1=82.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(174,1))]  ;
% DSSText.Command = ['New Load.DGP82c phases=1 bus1=82.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(175,1))]  ;
% %(90)
% DSSText.Command = ['New Load.DGP83a phases=1 bus1=83.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(176,1))]  ;
% DSSText.Command = ['New Load.DGP83b phases=1 bus1=83.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(177,1))]  ;
% DSSText.Command = ['New Load.DGP83c phases=1 bus1=83.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(178,1))]  ;
% %(91)
% DSSText.Command = ['New Load.DGP84c phases=1 bus1=84.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(179,1))]  ;
% %(92)
% DSSText.Command = ['New Load.DGP85c phases=1 bus1=85.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(180,1))]  ;
% %(93)
% DSSText.Command = ['New Load.DGP86a phases=1 bus1=86.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(181,1))]  ;
% DSSText.Command = ['New Load.DGP86b phases=1 bus1=86.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(182,1))]  ;
% DSSText.Command = ['New Load.DGP86c phases=1 bus1=86.3 kV=2.4 Model=1  pf=1  Kw=' num2str(p_inj(183,1))]  ;
% %(94)
% DSSText.Command = ['New Load.DGP87a phases=1 bus1=87.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(184,1))]  ;
% DSSText.Command = ['New Load.DGP87b phases=1 bus1=87.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(185,1))]  ;
% DSSText.Command = ['New Load.DGP87c phases=1 bus1=87.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(186,1))]  ;
% %(95)
% DSSText.Command = ['New Load.DGP88a phases=1 bus1=88.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(187,1))]  ;
% %(96)
% DSSText.Command = ['New Load.DGP89a phases=1 bus1=89.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(188,1))]  ;
% DSSText.Command = ['New Load.DGP89b phases=1 bus1=89.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(189,1))]  ;
% DSSText.Command = ['New Load.DGP89c phases=1 bus1=89.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(190,1))]  ;
% %(97)
% DSSText.Command = ['New Load.DGP90b phases=1 bus1=90.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(191,1))]  ;
% %(98)
% DSSText.Command = ['New Load.DGP91a phases=1 bus1=91.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(192,1))]  ;
% DSSText.Command = ['New Load.DGP91b phases=1 bus1=91.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(193,1))]  ;
% DSSText.Command = ['New Load.DGP91c phases=1 bus1=91.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(194,1))]  ;
% %(99)
% DSSText.Command = ['New Load.DGP92c phases=1 bus1=92.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(195,1))]  ;
% %(100)
% DSSText.Command = ['New Load.DGP93a phases=1 bus1=93.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(196,1))]  ;
% DSSText.Command = ['New Load.DGP93b phases=1 bus1=93.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(197,1))]  ;
% DSSText.Command = ['New Load.DGP93c phases=1 bus1=93.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(198,1))]  ;
% %(101)
% DSSText.Command = ['New Load.DGP94a phases=1 bus1=94.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(199,1))]  ;
% %(102)
% DSSText.Command = ['New Load.DGP95a phases=1 bus1=95.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(200,1))]  ;
% DSSText.Command = ['New Load.DGP95b phases=1 bus1=95.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(201,1))]  ;
% DSSText.Command = ['New Load.DGP95c phases=1 bus1=95.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(202,1))]  ;
% %(103)
% DSSText.Command = ['New Load.DGP96b phases=1 bus1=96.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(203,1))]  ;
% %(104)
% DSSText.Command = ['New Load.DGP97a phases=1 bus1=97.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(204,1))]  ;
% DSSText.Command = ['New Load.DGP97b phases=1 bus1=97.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(205,1))]  ;
% DSSText.Command = ['New Load.DGP97c phases=1 bus1=97.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(206,1))]  ;
% %(105)
% DSSText.Command = ['New Load.DGP98a phases=1 bus1=98.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(207,1))]  ;
% DSSText.Command = ['New Load.DGP98b phases=1 bus1=98.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(208,1))]  ;
% DSSText.Command = ['New Load.DGP98c phases=1 bus1=98.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(209,1))]  ;
% %(106)
% DSSText.Command = ['New Load.DGP99a phases=1 bus1=99.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(210,1))]  ;
% DSSText.Command = ['New Load.DGP99b phases=1 bus1=99.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(211,1))]  ;
% DSSText.Command = ['New Load.DGP99c phases=1 bus1=99.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(212,1))]  ;
% %(107)
% DSSText.Command = ['New Load.DGP100a phases=1 bus1=100.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(213,1))]  ;
% DSSText.Command = ['New Load.DGP100b phases=1 bus1=100.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(214,1))]  ;
% DSSText.Command = ['New Load.DGP100c phases=1 bus1=100.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(215,1))]  ;
% %(108)
% DSSText.Command = ['New Load.DGP450a phases=1 bus1=450.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(216,1))]  ;
% DSSText.Command = ['New Load.DGP450b phases=1 bus1=450.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(217,1))]  ;
% DSSText.Command = ['New Load.DGP450c phases=1 bus1=450.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(218,1))]  ;
% 
% %(110)
% DSSText.Command = ['New Load.DGP101a phases=1 bus1=101.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(219,1))]  ;
% DSSText.Command = ['New Load.DGP101b phases=1 bus1=101.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(220,1))]  ;
% DSSText.Command = ['New Load.DGP101c phases=1 bus1=101.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(221,1))]  ;
% %(111)
% DSSText.Command = ['New Load.DGP102c phases=1 bus1=102.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(222,1))]  ;
% %(112)
% DSSText.Command = ['New Load.DGP103c phases=1 bus1=103.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(223,1))]  ;
% %(113)
% DSSText.Command = ['New Load.DGP104c phases=1 bus1=104.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(224,1))]  ;
% %(114)
% DSSText.Command = ['New Load.DGP105a phases=1 bus1=105.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(225,1))]  ;
% DSSText.Command = ['New Load.DGP105b phases=1 bus1=105.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(226,1))]  ;
% DSSText.Command = ['New Load.DGP105c phases=1 bus1=105.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(227,1))]  ;
% %(115)
% DSSText.Command = ['New Load.DGP106b phases=1 bus1=106.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(228,1))]  ;
% %(116)
% DSSText.Command = ['New Load.DGP107b phases=1 bus1=107.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(229,1))]  ;
% %(117)
% DSSText.Command = ['New Load.DGP108a phases=1 bus1=108.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(230,1))]  ;
% DSSText.Command = ['New Load.DGP108b phases=1 bus1=108.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(231,1))]  ;
% DSSText.Command = ['New Load.DGP108c phases=1 bus1=108.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(232,1))]  ;
% %(118)
% DSSText.Command = ['New Load.DGP109a phases=1 bus1=109.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(233,1))]  ;
% %(119)
% DSSText.Command = ['New Load.DGP110a phases=1 bus1=110.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(234,1))]  ;
% %(120)
% DSSText.Command = ['New Load.DGP111a phases=1 bus1=111.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(235,1))]  ;
% %(121)
% DSSText.Command = ['New Load.DGP112a phases=1 bus1=112.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(236,1))]  ;
% %(122)
% DSSText.Command = ['New Load.DGP113a phases=1 bus1=113.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(237,1))]  ;
% %(123)
% DSSText.Command = ['New Load.DGP114a phases=1 bus1=114.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(238,1))]  ;
% 
% %(124)
% DSSText.Command = ['New Load.DGP300a phases=1 bus1=300.1 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(239,1))]  ;
% DSSText.Command = ['New Load.DGP300b phases=1 bus1=300.2 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(240,1))]  ;
% DSSText.Command = ['New Load.DGP300c phases=1 bus1=300.3 kV=2.4  Model=1  pf=1 Kw=' num2str(p_inj(241,1))]  ;
% 
% 




DSSCircuit      = DSSObj.ActiveCircuit;
DSSSolution     = DSSCircuit.Solution;
DSSSolution.Solve;

% busvoltages = DSSCircuit.AllBusVmag();
% busvoltages=busvoltages/2401;
V_phase1=DSSCircuit.AllNodeVmagPUByPhase(1);
V_phase2=DSSCircuit.AllNodeVmagPUByPhase(2);
V_phase3=DSSCircuit.AllNodeVmagPUByPhase(3);
% DSSText.Command='Show Voltages LN nodes';
% DSSText.Command='Show Powers Elem';
% Node_sequence=[1 3 4 7 5 6 8 9 11 12 2 13 10];
% Opendss node sequence
% 149,1,2,3,7,4,5,6,8,12,9,13,14,34,18,11,10,15,16,17,19,21,20,22,23,24,25,26,28,27,31,33,29,30,250,32,35,36,40,37,38,39,41,42,43,44,45,47,46,49,50,51,151,52,53,54,55,57,56,58,60,
% 59,61,62,63,64,65,66,67,68,72,97,69,70,71,73,76,74,75,77,86,78,79,80,81,82,84,83,85,87,88,89,90,91,92,93,94,95,96,98,99,100,450,197,101,102,105,103,104,106,108,109,300,110,111,112,113,114,135,152,160,610]

%Node sequence in my code(150=1,149,2...50=54..160=74)
% Node_sequence=[1 2 3 4 5 9 6 7 8 10 14 11 15 16 37 20 13 12 17 18 19 21 23 22 24 25 26 27 28 30 29 34 36 31 32 33 35 39 40 44 41 42 43 45 46 47 48 49 51 50 52 53 54 55 56 58 59 60 61 63 62 64 66 65 67 69 70 71 72 73 75 76 80 105 77 78 79 81 84 82 83 85 94 86 87 88 89 90 92 91 93 95 96 97 98 99 100 101 102 103 104 106 107 108 109 110 111 112 115 113 114 116 118 117 119 125 120 121 122 123 124 38 57 74 68];
Node_sequence=    [1  2  3  4 8 5 6 7 9 13 10 14 15 36 19 12 11 16 17 18 20 22 21 23 24 25 26 27 29 28 33 35 30 31 32 34  37 38 42 39 40 41 43 44 45 46 47 49 48 50 51 52 53 54  55 56 57 58 60 59 61 63 62 64 65 66 67 68 69 70 71 75 100 72 73 74 76  79 77 78 80 89 81 82 83 84 85 87 86 88 90 91 92 93 94 95 96 97 98 99 101 102 103 104  105 106 109 107 108 110 112 111  113 119  114 115 116 117 118 ];
%Nodeseq_Opendss=[149 1  2  3 7 4 5 6 8 12 9  13 14 34 18 11 10 15 16 17 19 21 20 22 23 24 25 26 28 27 31 33 29 30 250 32 35 36 40 37 38 39 41 42 43 44 45 47 46 48 49 50 51 151 52 53 54 55 57 56 58 60 59,61,62,63,64,65,66,67,68,72,97, 69,70,71,73, 76,74,75,77,86,78,79,80,81,82,84,83,85,87,88,89,90,91,92,93,94,95,96,98, 99, 100,450, 101,102,105,103,104,106,108,107 ,109,300, 110,111,112,113,114]
% compute phase_A_sequence
phase_number=Data.phase_number;
m=1;
for h=1:length(Node_sequence)
    if phase_number(Node_sequence(h),2)~=0
        phase_A_sequence(m)= phase_number(Node_sequence(h),2);
        m=m+1;
    end
end


% compute phase_B_sequence
m=1;
for h=1:length(Node_sequence)
    if phase_number(Node_sequence(h),3)~=0
        phase_B_sequence(m)= phase_number(Node_sequence(h),3);
        m=m+1;
    end
end

% compute phase_C_sequence
m=1;
for h=1:length(Node_sequence)
    if phase_number(Node_sequence(h),4)~=0
        phase_C_sequence(m)= phase_number(Node_sequence(h),4);
        m=m+1;
    end
end

% Finding the actual voltage measurement
V_measured=zeros(1,length(phase_A_sequence)+length(phase_B_sequence)+length(phase_C_sequence));
for h=1:length(phase_A_sequence)
    V_measured(phase_A_sequence(h))=V_phase1(h);
end

for h=1:length(phase_B_sequence)
    V_measured(phase_B_sequence(h))=V_phase2(h);
end

for h=1:length(phase_C_sequence)
    V_measured(phase_C_sequence(h))=V_phase3(h);
end

V_phase_OPENDSS=V_measured';

% Exclude the substation bus voltages

for h=1:Data.phases_node(Data.substation_bus)
   substation_phase(h,1)= phase_number(Data.substation_bus,h+1);
end
 V_phase_OPENDSS=V_phase_OPENDSS((substation_phase(end)+1):end,1);
    

end
end


