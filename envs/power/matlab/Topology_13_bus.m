
clc
clear all
Data.VBase = (4.16e3)/sqrt(3); % per phase base voltage (kV)
Data.SBase = 1000e3;% Per phase base power = 1000kVA
Data.ZBase =  Data.VBase^2/Data.SBase; % Ohms (per phase)
Data.SAdjCon = 10e6./Data.SBase; % Line Thermal Limits

Data.Vlb = 0.9;
Data.Vub = 1.1;
Data.substation_bus=1; % Substation bus =1

% netEdges =[from bus; to bus; Rij;Xij]

% Configuration of phases in the network
% fIDs = fopen('node_phases.txt');
fIDs = fopen('Line_Data_13_feeder.txt');
Line1=textscan(fIDs, '%f %s %s %s',1);

% A data structure named'data' is created
Data.N=Line1{1,1}; % Number of buses in the feeder
% N = Line1{1,1};
Line1={};
Line1=textscan(fIDs, '%s %s %s %s %s %s',1);
for h=1:Data.N
Phase_Data=textscan(fIDs, '%f %s %f %f %f %f',1);
Data.phases_node(h,1)=Phase_Data{1,3};
for t=1:3
Data.phase_node_config(h,t)=Phase_Data{1,3+t};
end
end

% Line1={};
% Line1= textscan(fIDs, '%s %s %s %s %s %s %s %s %s %s',1);
% for h=1:Data.N-1
%     Phase_Data=textscan(fIDs, '%f %f %s %f %f %f %f ',1);
%     Data.phases_branch(h,1)=Phase_Data{1,4};
% %     line_length(h,1)=Phase_Data{1,8}/5280; % 1 mile=5280 feet
%     for t=1:3
%     Data.phase_branch_config(h,t)=Phase_Data{1,4+t};
%     end
% end

% Conductor Data of the Network

Line1={};
Line1= textscan(fIDs,'%s %s %s %s %f', 1);
Data.Diff_conductor=Line1{1,5};
Line1= textscan(fIDs,'%s %s %s %s %s %s %s %s', 1);

    
% for k=1:Data.Diff_conductor
    Conductor_Data=textscan(fIDs,'%f %s %f %f %f %f %f %f', 1);
    count=0;
    while count<Data.Diff_conductor
        if isequal(Conductor_Data{1,1},601)
            count=count+1;
            for h=1:3
                for g=1:3
                    
                    Data.Conductor601.Res(h,g)=Conductor_Data{1,g*2+1};
                    
                    Data.Conductor601.Reactance(h,g)=Conductor_Data{1,2*g+2};
                end
                Conductor_Data=textscan(fIDs,'%f %s %f %f %f %f %f %f', 1);
            end
            
            
            
            
        elseif Conductor_Data{1,1}==602
            count=count+1;
            for h=1:3
                for g=1:3
                    Data.Conductor602.Res(h,g)=Conductor_Data{1,g*2+1};
                    Data.Conductor602.Reactance(h,g)=Conductor_Data{1,2*g+2};
                end
                Conductor_Data=textscan(fIDs,'%f %s %f %f %f %f %f %f', 1);
            end
            
            
            
            
        elseif isequal(Conductor_Data{1,1},603)
            count=count+1;
            for h=1:3
                for g=1:3
                    Data.Conductor603.Res(h,g)=Conductor_Data{1,g*2+1};
                    Data.Conductor603.Reactance(h,g)=Conductor_Data{1,2*g+2};
                end
                Conductor_Data=textscan(fIDs,'%f %s %f %f %f %f %f %f', 1);
            end
            
            
            
            
        elseif isequal(Conductor_Data{1,1},604)
            count=count+1;
            for h=1:3
                for g=1:3
                    Data.Conductor604.Res(h,g)=Conductor_Data{1,g*2+1};
                    Data.Conductor604.Reactance(h,g)=Conductor_Data{1,2*g+2};
                end
                Conductor_Data=textscan(fIDs,'%f %s %f %f %f %f %f %f', 1);
            end
            
            
            
            
        elseif isequal(Conductor_Data{1,1},605)
            count=count+1;
            for h=1:3
                for g=1:3
                    Data.Conductor605.Res(h,g)=Conductor_Data{1,g*2+1};
                    Data.Conductor605.Reactance(h,g)=Conductor_Data{1,2*g+2};
                end
                Conductor_Data=textscan(fIDs,'%f %s %f %f %f %f %f %f', 1);
            end
            
            
            
        elseif isequal(Conductor_Data{1,1},606)
            count=count+1;
            for h=1:3
                for j=1:3
                    Data.Conductor606.Res(h,j)=Conductor_Data{1,j*2+1};
                    Data.Conductor606.Reactance(h,j)=Conductor_Data{1,2*j+2};
                end
                Conductor_Data=textscan(fIDs,'%f %s %f %f %f %f %f %f', 1);
            end
            
            
            
            
        elseif isequal(Conductor_Data{1,1},607)
            count=count+1;
            for h=1:3
                for j=1:3
                    Data.Conductor607.Res(h,j)=Conductor_Data{1,j*2+1};
                    Data.Conductor607.Reactance(h,j)=Conductor_Data{1,2*j+2};
                end
                Conductor_Data=textscan(fIDs,'%f %s %f %f %f %f %f %f', 1);
            end
            
            
            
            
        elseif isequal(Conductor_Data{1,1},99)
            count=count+1;
            for h=1:3
                for j=1:3
                    Data.Conductor99.Res(h,j)=Conductor_Data{1,j*2+1};
                    Data.Conductor99.Reactance(h,j)=Conductor_Data{1,2*j+2};
                end
                Conductor_Data=textscan(fIDs,'%f %s %f %f %f %f %f %f', 1);
            end
            
            
            
        end
    end

    
% end

 % Branch Data
Data.Num_Branch=Conductor_Data{1,1}; % Number of branches in the system 
% Conductor_Data={};
Line1={};
Line1=textscan(fIDs,'%s ',1);
Line1=textscan(fIDs,'%s %s %s %s %s %s %s %s %s %s %s %s %s %s',1);

for  h=1:Data.Num_Branch
    Conductor_Data= textscan(fIDs,'%f %f %f %s %f %f %f %f %f %f ',1);
    Data.Branch_index(h,1)=Conductor_Data{1,1};
    Data.From_Bus(h,1)=Conductor_Data{1,2};
    Data.To_Bus(h,1)=Conductor_Data{1,3};
    Data.phases_branch(h,1)=Conductor_Data{1,5};
    for t=1:3
    Data.phase_branch_config(h,t)=Conductor_Data{1,5+t};
    end
    Data.Conductor_name_branch(h,1)=Conductor_Data{1,9};
    Data.Branch_length(h,1)=Conductor_Data{1,10};
    
    if isequal(Data.Conductor_name_branch(h,1),601)
        Data.R_matrix(Data.Branch_index(h,1),:,:)=(1/Data.ZBase)*(Data.Branch_length(h,1)/5280)*(Data.Conductor601.Res);
        Data.X_matrix(Data.Branch_index(h,1),:,:)=(1/Data.ZBase)*(Data.Branch_length(h,1)/5280)*(Data.Conductor601.Reactance);
    end
    
    if isequal(Data.Conductor_name_branch(h,1),602)
        Data.R_matrix(Data.Branch_index(h,1),:,:)=(1/Data.ZBase)*(Data.Branch_length(h,1)/5280)*(Data.Conductor602.Res);
        Data.X_matrix(Data.Branch_index(h,1),:,:)=(1/Data.ZBase)*(Data.Branch_length(h,1)/5280)*(Data.Conductor602.Reactance);
    end
    
    if isequal(Data.Conductor_name_branch(h,1),603)
        Data.R_matrix(Data.Branch_index(h,1),:,:)=(1/Data.ZBase)*(Data.Branch_length(h,1)/5280)*(Data.Conductor603.Res);
        Data.X_matrix(Data.Branch_index(h,1),:,:)=(1/Data.ZBase)*(Data.Branch_length(h,1)/5280)*(Data.Conductor603.Reactance);
    end
    
    if isequal(Data.Conductor_name_branch(h,1),604)
        Data.R_matrix(Data.Branch_index(h,1),:,:)=(1/Data.ZBase)*(Data.Branch_length(h,1)/5280)*(Data.Conductor604.Res);
        Data.X_matrix(Data.Branch_index(h,1),:,:)=(1/Data.ZBase)*(Data.Branch_length(h,1)/5280)*(Data.Conductor604.Reactance);
    end
    
    if isequal(Data.Conductor_name_branch(h,1),605)
        Data.R_matrix(Data.Branch_index(h,1),:,:)=(1/Data.ZBase)*(Data.Branch_length(h,1)/5280)*(Data.Conductor605.Res);
        Data.X_matrix(Data.Branch_index(h,1),:,:)=(1/Data.ZBase)*(Data.Branch_length(h,1)/5280)*(Data.Conductor605.Reactance);
    end
    
    if isequal(Data.Conductor_name_branch(h,1),606)
        Data.R_matrix(Data.Branch_index(h,1),:,:)=(1/Data.ZBase)*(Data.Branch_length(h,1)/5280)*(Data.Conductor606.Res);
        Data.X_matrix(Data.Branch_index(h,1),:,:)=(1/Data.ZBase)*(Data.Branch_length(h,1)/5280)*(Data.Conductor606.Reactance);
    end
    
    if isequal(Data.Conductor_name_branch(h,1),607)
        Data.R_matrix(Data.Branch_index(h,1),:,:)=(1/Data.ZBase)*(Data.Branch_length(h,1)/5280)*(Data.Conductor607.Res);
        Data.X_matrix(Data.Branch_index(h,1),:,:)=(1/Data.ZBase)*(Data.Branch_length(h,1)/5280)*(Data.Conductor607.Reactance);
    end
    
    if isequal(Data.Conductor_name_branch(h,1),99)
        Data.R_matrix(Data.Branch_index(h,1),:,:)=(1/Data.ZBase)*(Data.Branch_length(h,1)/5280)*(Data.Conductor99.Res);
        Data.X_matrix(Data.Branch_index(h,1),:,:)=(1/Data.ZBase)*(Data.Branch_length(h,1)/5280)*(Data.Conductor99.Reactance);
    end
    
    
end

% Net generation in the system
% fIDs = fopen('Net_gen.txt');
Line1= textscan(fIDs,'%s %s %s %s %s %s %s ', 1);
Line1=textscan(fIDs,'%s %s %s %s %s %s %s', 1);
for h=1:Data.N
    Line1= textscan(fIDs,'%f %6f %6f %6f %6f %6f %6f ', 1);
    for g=1:3
    Data.P_gen_matrix(h,g)=Line1{1,g+1}*1000/Data.SBase;
    Data.Q_gen_matrix(h,g)=Line1{1,g+4}*1000/Data.SBase;
    end
end
% Net loads in the system
% fIDs = fopen('Net_loads.txt');
Line1= textscan(fIDs,'%s %s %s %s %s %s %s ', 1);
Line1=textscan(fIDs,'%s %s %s %s %s %s %s', 1);
for h=1:Data.N
   Line1= textscan(fIDs,'%f %f %6f %6f %6f %6f %6f ', 1);
    for g=1:3
    Data.P_load_matrix(h,g)=Line1{1,g+1}*1000/Data.SBase;
    Data.Q_load_matrix(h,g)=Line1{1,g+4}*1000/Data.SBase;
    end
end
 % Mulitplying factor
 Line1=textscan(fIDs, '%s %s %.10f',1);
 
 Data.mult=Line1{1,3};
 Data.P_load_matrix=Data.mult*Data.P_load_matrix;
 Data.Q_load_matrix=Data.mult*Data.Q_load_matrix;
 
% ZIP Load modelling of loads connected in the system
Line1= textscan(fIDs,'%s %s %s %s %s %s %s ', 1);
for h=1:Data.N
    Line1= textscan(fIDs,'%f %f %6f %6f %6f %6f %6f ', 1);
    for g=1:2 % for both active and reactive power fractions
    Data.Impedance_fraction(h,g)=Line1{1,(g-1)*3+2};
    Data.Current_fraction(h,g)=Line1{1,(g-1)*3+3};
    Data.Power_fraction(h,g)=Line1{1,(g-1)*3+4};
    end
end
% Capacitors in the Network
Line1= textscan(fIDs,'%s %s %s %s %s %s %s ', 1);
Line1= textscan(fIDs,'%s %s %s %s', 1);

for h=1:Data.N
    Line1= textscan(fIDs,'%f %10.6f %10.6f %10.6f  ', 1);
    for g=1:3
        Data.Q_cap(h,g)=Line1{1,g+1}*1000/Data.SBase;
    end
end
 % CVR Factors for the network
 Line1=textscan(fIDs,'%s %s', 1);
 Line1=textscan(fIDs,'%f %f', 1);
 Data.CVR_P=Line1{1,1};
 Data.CVR_Q=Line1{1,2};
 
% Incorporation of DGs in the network
Line1= textscan(fIDs,'%s %s %s %s %s %s %s ', 1);
Line1= textscan(fIDs,'%s %s %s %s', 1);

for h=1:Data.N
    Line1= textscan(fIDs,'%f %10.6f %10.6f %10.6f  ', 1);
    for g=1:4
       Data.DG_bus(h,g)=Line1{1,g};
    end
end

% Incorporation of voltage regulator
Line1= textscan(fIDs,'%f %s %s %s %s %s', 1);
Data.Reg_number=Line1{1,1};
Line1=textscan(fIDs,'%s %s %s %s %s %s %s',1);

for h=1:Data.Reg_number
    Line1= textscan(fIDs,'%f %10.6f %10.6f %10.6f %f ', 1);
        Data.From_bus_reg(h,1)=Line1{1,1};
        Data.To_bus_reg(h,1)=Line1{1,2};
        for g=1:3
        Data.phases_reg(h,g)=Line1{1,g+2};
        end
   
end

 