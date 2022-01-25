% OPTDIST VC for 13 bus system
% Algorithm 1 Three Phase Model
% Without capacitors and regulators



% NETWORK
% MODEL.............................................................................

global T

Topology_123_bus_reg

[D_P,D_Q,Ao,D_p_abc,D_q_abc,Data] = gen_ZP_ZQ(Data); % G.R_matrix =D_P , G.X_matrix=D_Q

% Defining matrices
G.R_matrix=D_P;
G.X_matrix=D_Q;

G.Y_matrix=inv(G.X_matrix);  % Remove the unused phases
G.n = length(G.X_matrix(:,1));  % the number of control phases (buses*their own phases)  in the network ie. number of control agents present in the system

%................................%




% Network initialization

Data.N=119; % 123 bus feeder


%........Defining voltage and reactive power bounds for algorithm
Data.v_bar = 1.05^2; % upper limit for v
Data.v_un = 0.95^2; % lower limit for v


Data.q_bar = +1;% upper limit for q
Data.q_un  = -1; % lower limit for q

 Data.load_var = 1; % 100% loading

 % Defining the simulation case
simu_case = 'static';  % static or dynamic  or static_param(paramter sensitivity under static conditions)
q_control='fixed'; % fixed or all or all_control
 % if there are only fixed voltage controllers
% controllable nodes
if(strcmp(q_control, 'fixed')==1)
    
        q_gen_nodes=[14 26 54 63 105 89 99 118 104 88];% a subset of nodes are controllable
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
% Data.pq_fluc=0;
% Data.measurement=0;
% Data.delay=0;
% Data.volt=0;

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

% Normalizing Y_control
% finding appropriate Y for calculation
Y=G.Y_control;
for k1=1:length(Y(1,:))
    for k2=1:length(Y(:,1))
        %         if Y(k1,k2)<=10E-03
        if abs(Y(k1,k2))<=10E-03
            Y(k1,k2)=0;
        end
    end
end
% under scaling
for k=1:length(Y(1,:))
    D(k,1)=max(abs(Y(k,:)));
end
Y_max=max(D);
Y=(1/Y_max)*Y;
G.Y_control=Y;

% size of network
n = size(Data.q_un_vec,1); % number of controllable nodes

global var

var.q_hat = zeros(n,T); % ''virtual'' reactive power
var.xi = zeros(n,T); % lagrangian multiplier for reactive power constraint
var.lambda_bar = zeros(n,T); % lagrangian multipler for voltage constraint (upper limit)
var.lambda_un = zeros(n,T); % lagrangian multipler for voltage constraint (lower limit)
var.v_c = zeros(n,T); % voltage
var.v_c_phase = zeros(n,T); % voltage
var.q = zeros(n,T); % ''actual'' reactive power
var.f = zeros(1,T); % objective function value
var.fes = zeros(1,T); % feasibility of solution

global g_data control_flag delay delay_flag measurement_noise noise_flag power_loss_ratio load_var v_un v_bar q_un q_bar a b Y C U_c
g_data = Data
control_flag = 1
delay = 0;
delay_flag = 0
measurement_noise = 0
noise_flag = 0
power_loss_ratio = Data.power_loss_weight
load_var = Data.load_var

v_un=Data.v_un_vec;
v_bar=Data.v_bar_vec;
q_un=Data.q_un_vec;
q_bar=Data.q_bar_vec;
a=Data.a;
b=Data.b;
Y=G.Y_control;

% size of network
U_c=G.U_c;
% only for control nodes
v_un=G.C*v_un;
v_bar=G.C*v_bar;

C=G.C;
