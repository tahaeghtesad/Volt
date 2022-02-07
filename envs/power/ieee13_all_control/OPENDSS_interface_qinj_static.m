function [V_phase_OPENDSS] = OPENDSS_interface_qinj_static(t,load_var,q_inj,Data)
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here

[DSSStartOK, DSSObj, DSSText] = DSSStartup;

if DSSStartOK

DSSObj.AllowForms = false;
DSSText.Command = 'Set DataPath =C:\Users\teghtesa\PycharmProjects\Volt\envs\power\ieee13_all_control';
DSSText.Command = 'Compile IEEE13Nodeckt.dss';
lm=load_var;
% lm=1.2;
DSSText.Command=['set mode =snap loadmult=' num2str(lm)];
% fileID0=fopen('MyFile0.txt','w');
% fprintf(fileID0,'set mode=snap loadmult = %d',lm);
% formatSpec = '%c';
% fileID0_0 = fopen('MyFile0.txt','r');
% loadmult = fscanf(fileID0_0,formatSpec);
% DSSText.Command = loadmult;
% fclose(fileID0);
% fclose(fileID0_0);

% Adding reactive power generators
% For 13 bus feeder (MATLAB code)
% 650=1, 632=2, 633=3, 634=4, 645=5, 646=6, 671=7, 692=8, 675=9, 684=10,
% 611=11, 652=12, 680=13

% But in OPENDSS
% the voltage magnitudes are arranged in this form
% 650,633,634,671,645,646,692,675,611,652,632,680,684--which if arranged ==
% 1,3,4,7,5,6,8,9,11,12,2,13,10
%q_inj is the amount of reactive power that neesds to be injected by the
%generators

q_inj=q_inj*1000;
DSSText.Command = ['New Generator.DG632a phases=1 bus1=632.1 kV=2.4  Kw=0 kvar=' num2str(q_inj(1,1))]  ;
DSSText.Command = ['New Generator.DG632b phases=1 bus1=632.2 kV=2.4  Kw=0 kvar=' num2str(q_inj(2,1))]  ;
DSSText.Command = ['New Generator.DG632c phases=1 bus1=632.3 kV=2.4  Kw=0 kvar=' num2str(q_inj(3,1))]  ;

DSSText.Command = ['New Generator.DG633a phases=1 bus1=633.1 kV=2.4  Kw=0 kvar=' num2str(q_inj(4,1))]  ;
DSSText.Command = ['New Generator.DG633b phases=1 bus1=633.2 kV=2.4  Kw=0 kvar=' num2str(q_inj(5,1))]  ;
DSSText.Command = ['New Generator.DG633c phases=1 bus1=633.3 kV=2.4  Kw=0 kvar=' num2str(q_inj(6,1))]  ;
DSSText.Command = ['New Generator.DG634a phases=1 bus1=634.1 kV=2.4 Kw=0 kvar=' num2str(q_inj(7,1))]  ;
DSSText.Command = ['New Generator.DG634b phases=1 bus1=634.2 kV=2.4  Kw=0 kvar=' num2str(q_inj(8,1))]  ;
DSSText.Command = ['New Generator.DG634c phases=1 bus1=634.3 kV=2.4 Kw=0 kvar=' num2str(q_inj(9,1))]  ;

DSSText.Command = ['New Generator.DG645b phases=1 bus1=645.2 kV=2.4  Kw=0 kvar=' num2str(q_inj(10,1))]  ;
DSSText.Command = ['New Generator.DG645c phases=1 bus1=645.3 kV=2.4  Kw=0 kvar=' num2str(q_inj(11,1))]  ;


DSSText.Command = ['New Generator.DG646b phases=1 bus1=646.2 kV=2.4  Kw=0 kvar=' num2str(q_inj(12,1))]  ;
DSSText.Command = ['New Generator.DG646c phases=1 bus1=646.3 kV=2.4  Kw=0 kvar=' num2str(q_inj(13,1))]  ;

DSSText.Command = ['New Generator.DG671a phases=1 bus1=671.1 kV=2.4  Kw=0 kvar=' num2str(q_inj(14,1))]  ;
DSSText.Command = ['New Generator.DG671b phases=1 bus1=671.2 kV=2.4  Kw=0 kvar=' num2str(q_inj(15,1))]  ;
DSSText.Command = ['New Generator.DG671c phases=1 bus1=671.3 kV=2.4  Kw=0 kvar=' num2str(q_inj(16,1))]  ;

DSSText.Command = ['New Generator.DG692a phases=1 bus1=692.1 kV=2.4  Kw=0 kvar=' num2str(q_inj(17,1))]  ;
DSSText.Command = ['New Generator.DG692b phases=1 bus1=692.2 kV=2.4  Kw=0 kvar=' num2str(q_inj(18,1))]  ;
DSSText.Command = ['New Generator.DG692c phases=1 bus1=692.3 kV=2.4  Kw=0 kvar=' num2str(q_inj(19,1))]  ;

DSSText.Command = ['New Generator.DG675a phases=1 bus1=675.1 kV=2.4  Kw=0 kvar=' num2str(q_inj(20,1))]  ;
DSSText.Command = ['New Generator.DG675b phases=1 bus1=675.2 kV=2.4  Kw=0 kvar=' num2str(q_inj(21,1))]  ;
DSSText.Command = ['New Generator.DG675c phases=1 bus1=675.3 kV=2.4  Kw=0 kvar=' num2str(q_inj(22,1))]  ;

DSSText.Command = ['New Generator.DG684a phases=1 bus1=684.1 kV=2.4  Kw=0 kvar=' num2str(q_inj(23,1))]  ;
DSSText.Command = ['New Generator.DG684c phases=1 bus1=684.3 kV=2.4  Kw=0 kvar=' num2str(q_inj(24,1))]  ;

DSSText.Command = ['New Generator.DG611c phases=1 bus1=611.3 kV=2.4  Kw=0 kvar=' num2str(q_inj(25,1))]  ;

DSSText.Command = ['New Generator.DG652a phases=1 bus1=652.1 kV=2.4  Kw=0 kvar=' num2str(q_inj(26,1))]  ;

DSSText.Command = ['New Generator.DG680a phases=1 bus1=680.1 kV=2.4  Kw=0 kvar=' num2str(q_inj(27,1))]  ;
DSSText.Command = ['New Generator.DG680b phases=1 bus1=680.2 kV=2.4  Kw=0 kvar=' num2str(q_inj(28,1))]  ;
DSSText.Command = ['New Generator.DG680c phases=1 bus1=680.3 kV=2.4  Kw=0 kvar=' num2str(q_inj(29,1))]  ;








DSSCircuit      = DSSObj.ActiveCircuit;
DSSSolution     = DSSCircuit.Solution;
DSSSolution.Solve;

V_phase1=DSSCircuit.AllNodeVmagPUByPhase(1);
V_phase2=DSSCircuit.AllNodeVmagPUByPhase(2);
V_phase3=DSSCircuit.AllNodeVmagPUByPhase(3);
%  DSSText.Command='Show Voltages LN nodes';

Node_sequence=[1 3 4 7 5 6 8 9 11 12 2 13 10];
 phases_node_sequence=Data.phases_node(Node_sequence(:));
 V_phase_node=zeros(Data.N,3);
 V_phase_pu=DSSCircuit.AllBusVmagPU;
k1=1; 
k2=1;
k3=1;

for h=1:length(Node_sequence(1,:))
    
    for g=1:3
        
        if Data.phase_node_config(Node_sequence(h),g)~=0
            if g==1
                V_phase_node(Node_sequence(h),g)=V_phase1(k1);
                k1=k1+1;
            end
            
            if g==2
                V_phase_node(Node_sequence(h),g)=V_phase2(k2);
                k2=k2+1;
            end
            
            if g==3
                V_phase_node(Node_sequence(h),g)=V_phase3(k3);
                k3=k3+1;
            end
            
            
            
            
        end
    end
end

k=1;
for h=2:length(V_phase_node(:,1))
    for g=1:3
        if V_phase_node(h,g)~=0  % Only taking the non-substation voltages or feeder voltages
            V_phase_OPENDSS(k,1)=V_phase_node(h,g);
            k=k+1;
        end
    end
end

end
end

