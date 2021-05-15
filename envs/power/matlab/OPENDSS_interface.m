function [V_phase_OPENDSS] = OPENDSS_interface(load_var,Data,simu_case)
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here

[DSSStartOK, DSSObj, DSSText] = DSSStartup;



if DSSStartOK

    DSSObj.AllowForms = false;

      DSSText.Command = 'Set DataPath =C:\Users\Niloy\Dropbox\NILOY\LINA_MATLAB_CODES\Algorithm1_three_phase_extension\IEEE13BusFeeder';
    DSSText.Command = 'Compile IEEE13Nodeckt.dss';
    if (strcmp(simu_case, 'static')==1)
        lm=load_var;
        
        
        DSSCircuit      = DSSObj.ActiveCircuit;
        DSSSolution     = DSSCircuit.Solution;
        DSSSolution.Solve;
        
        
        % For 13 bus feeder (MATLAB code)
        % 650=1, 632=2, 633=3, 634=4, 645=5, 646=6, 671=7, 692=8, 675=9, 684=10,
        % 611=11, 652=12, 680=13
        
        % But in OPENDSS
        % the voltage magnitudes are arranged in this form
        % 650,633,634,671,645,646,692,675,611,652,632,680,684--which if arranged ==
        % 1,3,4,7,5,6,8,9,11,12,2,13,10
        V_phase1=DSSCircuit.AllNodeVmagPUByPhase(1);
        V_phase2=DSSCircuit.AllNodeVmagPUByPhase(2);
        V_phase3=DSSCircuit.AllNodeVmagPUByPhase(3);
        DSSText.Command='Export Voltages ';
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
%...........................................................................
if(strcmp(simu_case, 'dynamic')==1)
    for t=1:length(load_var{:,1})
        lm=load_var{t,2};
        
        
        
        DSSText.Command=['set mode =snap loadmult=' num2str(lm)];
        % fileID0=fopen('MyFile0.txt','w');
        % fprintf(fileID0,'set mode=snap loadmult = %d',lm);
        % formatSpec = '%c';
        % fileID0_0 = fopen('MyFile0.txt','r');
        % loadmult = fscanf(fileID0_0,formatSpec);
        % DSSText.Command = loadmult;
        
        DSSCircuit      = DSSObj.ActiveCircuit;
        DSSSolution     = DSSCircuit.Solution;
        DSSSolution.Solve;
        
        
        % For 13 bus feeder (MATLAB code)
        % 650=1, 632=2, 633=3, 634=4, 645=5, 646=6, 671=7, 692=8, 675=9, 684=10,
        % 611=11, 652=12, 680=13
        
        % But in OPENDSS
        % the voltage magnitudes are arranged in this form
        % 650,633,634,671,645,646,692,675,611,652,632,680,684--which if arranged ==
        % 1,3,4,7,5,6,8,9,11,12,2,13,10
        V_phase1=DSSCircuit.AllNodeVmagPUByPhase(1);
        V_phase2=DSSCircuit.AllNodeVmagPUByPhase(2);
        V_phase3=DSSCircuit.AllNodeVmagPUByPhase(3);
        DSSText.Command='Export Voltages ';
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
                    V_phase_OPENDSS(k,t)=V_phase_node(h,g);
                    k=k+1;
                end
            end
        end
        
        
        
        
        
        
    end
end





end
end

