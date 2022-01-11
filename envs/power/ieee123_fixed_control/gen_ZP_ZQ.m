function [D_P,D_Q,Ao,D_p_abc,D_q_abc,Data] = gen_ZP_ZQ(Data)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
sum_phases_branch=0;
% Add all phases
for h=1:Data.Num_Branch  % Number of nodes
    
    sum_phases_branch=sum_phases_branch+Data.phases_branch(h,1);
end

% Z_Q = zeros(sum_phases_branch,sum_phases_branch);
% Z_P = zeros(sum_phases_branch,sum_phases_branch);
Z_Q=[];
Z_P=[];
Data.branch=horzcat(Data.From_Bus,Data.To_Bus);

alpha=exp(-1i*2*pi/3);
for h=1:Data.Num_Branch
    for g=1:3
        for g1=1:3
            if g==1 
                if g1==1
            Data.Z_matrix(h,g,g1)=conj(Data.R_matrix(h,g,g1)+1i*Data.X_matrix(h,g,g1));
                end
                 if g1==2
                     Data.Z_matrix(h,g,g1)=alpha^2*(conj(Data.R_matrix(h,g,g1)+1i*Data.X_matrix(h,g,g1)));   
                 end   
                 if g1==3
                       Data.Z_matrix(h,g,g1)=alpha*(conj(Data.R_matrix(h,g,g1)+1i*Data.X_matrix(h,g,g1))); 
                 end
            end
            
            if g==2
                if g1==1
                    Data.Z_matrix(h,g,g1)=alpha*(conj(Data.R_matrix(h,g,g1)+1i*Data.X_matrix(h,g,g1)));
                end
                if g1==2
                     Data.Z_matrix(h,g,g1)=conj(Data.R_matrix(h,g,g1)+1i*Data.X_matrix(h,g,g1));
                end
                if g1==3
                    Data.Z_matrix(h,g,g1)=alpha^2*(conj(Data.R_matrix(h,g,g1)+1i*Data.X_matrix(h,g,g1))); 
                end
            end
            
            if g==3
                if g1==1
                    Data.Z_matrix(h,g,g1)=alpha^2*(conj(Data.R_matrix(h,g,g1)+1i*Data.X_matrix(h,g,g1)));
                end
                if g1==2
                    Data.Z_matrix(h,g,g1)=alpha*(conj(Data.R_matrix(h,g,g1)+1i*Data.X_matrix(h,g,g1)));
                end
                if g1==3
                    Data.Z_matrix(h,g,g1)=conj(Data.R_matrix(h,g,g1)+1i*Data.X_matrix(h,g,g1));
                end
            end
        end
    end
end

for j=1:Data.Num_Branch
    x_tmp=zeros(3,3);
    r_tmp=zeros(3,3);
    %     for k1 = 2:Data.N
    %         for k2 = 2:Data.N
    %             path1 = find_path_to_root(Data.branch(:,1:2),k1);
    %             path2 = find_path_to_root(Data.branch(:,1:2),k2);
    %             path = intersect(path1,path2);
    %             r_tmp = zeros(3,3);
    %             x_tmp = zeros(3,3);
    %             for kk = 1:length(path)-1
    %                 index_from_bus=find(Data.branch(:,1)==path(kk));
    %                 index_to_bus=find(Data.branch(:,2)==path(kk+1));
    %                 index=intersect(index_from_bus,index_to_bus);
    for h=1:3
        for g=1:3
            x_tmp(h,g) = x_tmp(h,g) +  2*real(1i*(Data.Z_matrix(j,h,g)));
            r_tmp(h,g)= r_tmp(h,g) + 2*real(Data.Z_matrix(j,h,g));
        end
    end
    
    z_p=[];
    z_q=[];
    ph_available=[];
    
    if Data.phases_branch(j)==3
                z_p=r_tmp;
                z_q=x_tmp;
    end
    if Data.phases_branch(j)==2
       for h=1:3
           if Data.phase_branch_config(j,h)~=0
               ph_available=horzcat(ph_available,Data.phase_branch_config(j,h));
           end
       end
%        com_phases=nchoosek(ph_available,2);
%        if length(ph_available)~=1
           m1=1;
           
       for h=1:length(ph_available)
           m2=1;
           z_p(m1,m2)=r_tmp(ph_available(m1),ph_available(m2));
           z_q(m1,m2)=x_tmp(ph_available(m1),ph_available(m2));
           m2=m2+1;
           z_p(m1,m2)=r_tmp(ph_available(m1),ph_available(m2));
           z_q(m1,m2)=x_tmp(ph_available(m1),ph_available(m2));
           m1=m1+1;
       end
            
        
        
    end
    
    if Data.phases_branch(j)==1
        for h=1:3
           if Data.phase_branch_config(j,h)~=0
        ph_available=Data.phase_branch_config(j,h);
           end
        end
    z_p=r_tmp( ph_available, ph_available);
    z_q=x_tmp( ph_available, ph_available);
    end
        
    
    Z_Q=blkdiag(Z_Q,z_q);
    Z_P=blkdiag(Z_P,z_p);
end
    
% finding full branch-node incidence matrix
node_phases=0;
for h=1:Data.N
    node_phases=node_phases+Data.phases_node(h);
end

% find the phase numbers for eahc node
%phase_number=[node phaseA phaseB phaseC]
phase_number=zeros(Data.N,4);
m1=1;
for h=1:Data.N
    phase_number(h,1)=h;
    for g=1:3
        if Data.phase_node_config(h,g)~=0
            phase_number(h,g+1)=m1;
            m1=m1+1;
        end
    end
end
A_incidence=zeros(sum_phases_branch,node_phases);
m1=1;
for h=1:Data.Num_Branch
    for g=1:3
        if Data.phase_branch_config(h,g)~=0
            A_incidence(m1,phase_number(Data.From_Bus(h),g+1))=1;  % outgoing current from bus
            A_incidence(m1,phase_number(Data.To_Bus(h),g+1))=-1;  % incoming current to bus
            m1=m1+1;
        end
    end
end

% Finding reduced incidence matrix
ao=A_incidence(:,1:Data.phases_node(1));
A_reduced_incidence=A_incidence(:,Data.phases_node(1)+1:end);

F=inv(A_reduced_incidence);
Ao=-F*ao;
D_P= F*Z_P*F';
D_Q=F*Z_Q*F';
Data.phase_number=phase_number;
Data.node_phases=node_phases;
phases_substation=Data.phases_node(Data.substation_bus);
Data.node_phases=Data.node_phases-phases_substation;
%...................................................................................................................................
% Let us construct the equation as following
% [Va Vb Vc]transpose= Vsubs+ Dabc_P*[Pinj_a_phase Pinj_b_phase Pinj_c_phase]transpose +Dabc_Q*[Qinj_a_phase Qinj_b_phase Qinj_c_phase]transpose
% Let, V=H*[Va Vb Vc]transpose
% Finding reduced phase_number
m1=1;
m_node=1;
for h=1:Data.N
    if h~=Data.substation_bus
        phase_number_reduced(m_node,1)=m_node;
        for g=1:3
            if Data.phase_node_config(h,g)~=0
                phase_number_reduced(m_node,g+1)=m1;
                m1=m1+1;
            end
        end
        m_node=m_node+1;
    end
    
end
Data.phase_number_reduced=phase_number_reduced;
m=1;
Data.phase_abc=zeros(length(Data.phase_number_reduced(:,1)),length(Data.phase_number_reduced(1,:)));
Data.phase_abc(:,1)=Data.phase_number_reduced(:,1);
for h=1:3
   for g=1:length(Data.phase_number_reduced(:,1))
      if Data.phase_number_reduced(g,h+1)~=0
            Data.phase_abc(g,h+1)=m;
            m=m+1;
      end
   end
end

H= zeros(length(D_Q(:,1)),length(D_Q(1,:)));
for h=1:3
   for g=1:length(Data.phase_number_reduced(:,1))
      if Data.phase_number_reduced(g,h+1)~=0
            H(Data.phase_abc(g,h+1),Data.phase_number_reduced(g,h+1))=1;
            m=m+1;
      end
   end
end
Data.H=H;

% New D_P and D_Q
D_p_abc=H*D_P*inv(H);
D_q_abc=H*D_Q*inv(H);


% function path = find_path_to_root (paths, node)
%     % find the path from 1 to node
%     path = node;
%     current = node; 
%     while 1
%         next_idx = find(paths(:,2) == current);
%         next = paths(next_idx,1);
%         path = [next,path];
%         if(next == 1)
%             break;
%         end
%         current = next;
%     end
% end
end

