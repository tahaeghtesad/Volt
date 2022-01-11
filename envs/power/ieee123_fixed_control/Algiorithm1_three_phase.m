% OPTDIST VC for 13 bus system
% Algorithm 1 Three Phase Model
% Without capacitors and regulators
clc;close all;



% NETWORK
% MODEL.............................................................................
% network data
Topology_13_bus

[D_P,D_Q,Ao,D_p_abc,D_q_abc,Data] = gen_ZP_ZQ(Data); % G.R_matrix =D_P , G.X_matrix=D_Q

% Defining matrices
G.R_matrix=D_P;
G.X_matrix=D_Q;

G.Y_matrix=inv(G.X_matrix);  % Remove the unused phases
G.n = length(G.X_matrix(:,1));  % the number of control phases (buses*their own phases)  in the network ie. number of control agents present in the system

%................................%




% Network initialization


Data.N=13; % 13 bus feeder
%........Defining voltage and reactive power bounds for algorithm
Data.v_bar = 1.05^2; % upper limit for v
Data.v_un = 0.95^2; % lower limit for v


Data.q_bar = +1;% upper limit for q
Data.q_un  = -1; % lower limit for q

 Data.load_var = 1; % 100% loading
 T=10000; % Number of iterations

 % Defining the simulation case
simu_case = 'static';  % static or dynamic  or static_param(paramter sensitivity under static conditions)
q_control='all_control'; % fixed or all or all_control
 % if there are only fixed voltage controllers
% controllable nodes
if(strcmp(q_control, 'fixed')==1)
    
    q_gen_nodes=[ 4 7 9 10]; % a subset of nodes are controllable
end

% for all DERs in each available phases of the network acting as voltage
% control agents
if(strcmp(q_control, 'all_control')==1)
    
    for k=1:Data.N-1 % excluding the substation node
        q_gen_nodes(1,k)=k+1;
    end
end

%...............
m=1;
for k=1:length(q_gen_nodes)
    for g=1:Data.phases_node(q_gen_nodes(k))
        G.phases_gen_nodes(m,1)=sum(Data.phases_node(2:q_gen_nodes(k)-1))+g; % ( control node phases) excluding the substation node
        m=m+1;
    end
end

% reactive power bounds on control nodes
G.phase_control_nodes=length(G.phases_gen_nodes);
Data.q_bar_vec = Data.q_bar*ones(G.phase_control_nodes,1);
Data.q_un_vec  = Data.q_un*ones(G.phase_control_nodes,1);



% voltage bounds on control nodes

Data.v_bar_vec = Data.v_bar*ones(G.n,1);
Data.v_un_vec  = Data.v_un*ones(G.n,1);

% All parameters for control nodes only
Data.c_price = 10;
Data.s_max = rand(G.phase_control_nodes,1)*0.5+0.5;
Data.a = zeros(G.phase_control_nodes,1);
Data.a(1:G.phase_control_nodes) = 2* Data.c_price./Data.s_max(1:G.phase_control_nodes);%ones(N,1);%1+rand(N,1);% ones(N,1);
%a = a.*(randi(2,n,1)-1); % some of the a_i will be set as zero for zero cost function
Data.b =  zeros(G.phase_control_nodes,1);
Data.power_loss_weight = 1 ; % can be put to 1

% to introduce measurement noises, delay
Data.pq_fluc=0;
Data.measurement=0;
Data.delay=0;
Data.volt=0;

% C*v=C*R*p+C*x*q+C*vo is equivalent to
% C*v=C*R*p+C*X*U_c*qc+C*X*U_unc*qunc+C*vo where
% q=U_c*qc+U_unc*q_unc
% for controllable nodes  %Rc=C*R, Xc=C*X, v0_c=C*vo
% Fnding q=U_c*q_c+U_unc*q_unc
G.U_c=zeros(G.n,G.phase_control_nodes);% for control phases
G.U_unc=zeros(G.n,G.n-G.phase_control_nodes); % all phases- control_phases


all_nodes=zeros(G.n,1);
for k=1:G.n
    G.phases_all_nodes(k,1)=k;
end
G.q_unc = setdiff( G.phases_all_nodes,G.phases_gen_nodes );
m=1;
for k=1:length(G.phases_gen_nodes)
    G.U_c(G.phases_gen_nodes(k),m)=1;
    m=m+1;
end


% finding U_unc
m=1;
for k=1:length(G.q_unc)
    G.U_unc(G.q_unc(k),m)=1;
    m=m+1;
end

%.........
G.C=zeros(length(G.phases_gen_nodes),G.n); % G.n=29

for m=1:length(G.phases_gen_nodes)
    G.C(m,G.phases_gen_nodes(m,1))=1; % popualting C Matrix
end

G.Rc_matrix=G.C*G.R_matrix;
G.Xc_matrix=G.C*G.X_matrix;
G.v0_c=G.C*ones(G.n,1); % substation end voltage

% finding actual matrices
%v_c=C*v=C*R*p+C*X*U_c*qc+C*X*U_unc*qunc+C*vo
G.X_control=G.Xc_matrix*G.U_c;
G.Y_control=inv(G.X_control);

% size of network
n = size(Data.q_un_vec,1); % number of controllable nodes

var.q_hat = zeros(n,T); % ''virtual'' reactive power
var.xi = zeros(n,T); % lagrangian multiplier for reactive power constraint
var.lambda_bar = zeros(n,T); % lagrangian multipler for voltage constraint (upper limit)
var.lambda_un = zeros(n,T); % lagrangian multipler for voltage constraint (lower limit)
var.v = zeros(n,T); % voltage
var.q = zeros(n,T); % ''actual'' reactive power
var.f = zeros(1,T); % objective function value
var.fes = zeros(1,T); % feasibility of solution
% Algorithm parameters
for t=1:T
Data.alpha = 10^(-3.7748); % 0.001
Data.beta = 10^(-3.5788); % 5
Data.gamma = 10^(3.734); %200
Data.c=10^(1.3238); %1




% [v,v_phase,v_c,v_c_phase, q,fes,f,lambda_bar,lambda_un,xi,q_hat] = Input_parameter(Data,G,T,t);

[var] = optdist_vc_static_control(T,Data,G,t,var);
end






% For 13 bus feeder ( in MATLAB code)
% 650=1, 632=2, 633=3, 634=4, 645=5, 646=6, 671=7, 692=8, 675=9, 684=10,
% 611=1, 652=12, 680=13

% when no scaling on Y is done, these are the parameters (static)
%     Data.alpha = 0.000002;
%      Data.beta = 0.05;
%     Data.gamma = 200000;

% PLOTS%................
 m1=1:1:T-1 ;
    figure;
    plot(m1,var.f(1:T-1),'k','Linewidth',2); % Actual voltages is found by taking sqaure root of v(:,12)
    % title('Bus 680  Voltage ');
    grid on;
    xlim([0 T]);
    xlabel('Iterations') ;
    ylabel('Objective value (pu)') ;
    %legend({'\alpha=0.00001','\alpha=0.01'},'Location','northeast');
    ax = gca;
    ax.FontSize = 16;
    figure;
    plot(m1,var.q(:,1:T-1),'Linewidth',2);
    grid on;
    xlabel('Iterations') ;
    xlim([0 T]);
    ylabel('Reactive power injections (pu)') ;
    %yticks([0.1 0.2 ]);
    %yticklabels({'0.1','0.2'});
    %legend({'V_{652} pu','q_{652} pu'},'Location','northeast');
    ax = gca;
    ax.FontSize = 16;
    
    
    figure;
    plot(m1,var.v_phase,'Linewidth',2);
    grid on;
    xlim([0 T]);
    xlabel('Iterations') ;
    ylabel('Bus voltages (pu)') ;
    %yticks([0.9 0.95 1.0 1.05]);
    %yticklabels({'0.9','0.95','1.0','1.05'});
    %legend({'V_{652} pu','q_{652} pu'},'Location','northeast');
    ax = gca;
    ax.FontSize = 16;





    

    
    
    
   
    
