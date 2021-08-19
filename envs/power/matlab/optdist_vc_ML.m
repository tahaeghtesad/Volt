function optdist_vc_ML(params, t)

    global g_data
    global g_T
    global g_G
    global var

Data = g_data;
T = g_T;
G = g_G;

%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here

% T - number of iterations
% stepsize - 3-vecotr containing value of alpha,beta,gamma
% v_un,v_bar: n-by-1 vector of voltage lower/upper bound
% q_un, q_bar: n-by-1 vector of quadratic power lower/upper bound
% volt: handle for solving PF
% a,b related to cost function
% Y: inv of X

% Parameters
v_un=Data.v_un_vec;
v_bar=Data.v_bar_vec;
q_un=Data.q_un_vec;
q_bar=Data.q_bar_vec;
a=Data.a;
b=Data.b;
power_loss_ratio=Data.power_loss_weight;
Y=G.Y_control;
measurement_noise=Data.measurement;
delay=Data.delay;
load_var=Data.load_var;



% var.v(:,t) = v(:,t); % voltage
% var.q = zeros(n,T); % ''actual'' reactive power
% var.f = zeros(1,T); % objective function value
% var.fes = zeros(1,T); % feasibility of solution

% size of network
n = size(q_un,1); % number of controllable nodes

% only for control nodes
v_un=G.C*v_un;
v_bar=G.C*v_bar;
% step sizes
alpha = params.alpha;
beta = params.beta;
gamma = params.gamma;
    
% if(nargin>=13)
%     noise_flag=1;
% else
    noise_flag=0;
% end


    delay_flag=0;
% end
control_flag=1;






c=params.c;% parameter for augmented Lagrangian

% projection functions
proj0 = @(r) max(r,zeros(size(r)));


% gradient handle
X = inv(Y);
nabla = @(qqq) a.*qqq + b ;
nabla_indvidual = @(qqq,jjj) a(jjj)*qqq+b(jjj);
f_func = @(qqq) sum(1/2*a.*(qqq.^2) + b.*qqq);



% Y=(1/1.68E4)*Y;
% eig_A = eig(Y);
% flag = 0;
% for i = 1:rank(Y)
%   if eig_A(i) <= 0 
%   flag = 1;
%   end
% end
% if flag == 1
%   disp('the matrix is not positive definite')
%   else
%   disp('the matrix is positive definite')
% end
% initialization for first iteration
    if t==1
        xi(:,t) =zeros(n,t); % for first iteration, xi=0
        q_hat(:,t)=zeros(n,t); % for first iteration, q_hat=0
        lambda_bar(:,t)=zeros(n,t);
        lambda_un(:,t)=zeros(n,t);
    else
        q_hat(:,t-1)= var.q_hat(:,t-1) ; % ''virtual'' reactive power
         xi(:,t)= var.xi(:,t) ; % lagrangian multiplier for reactive power constraint
        lambda_bar(:,t)= var.lambda_bar(:,t) ; % lagrangian multipler for voltage constraint (upper limit)
        lambda_un(:,t)= var.lambda_un(:,t)  ; % lagrangian multipler for voltage constraint (lower limit)
%         var.v = zeros(n,T); % voltage
%         var.q = zeros(n,T); % ''actual'' reactive power
%         var.f = zeros(1,T); % objective function value
%         var.fes = zeros(1,T); % feasibility of solution
    end
   

    if(t>1)
        if(delay_flag==0)
            GG = max(min(xi(:,t) + c.*(q_hat(:,t-1) - q_un),0), xi(:,t)+c.*(q_hat(:,t-1) - q_bar));
            comm_vector = nabla(q_hat(:,t-1)) + GG ;
            q_hat(:,t) = q_hat(:,t-1) - alpha.*(lambda_bar(:,t) - lambda_un(:,t) + power_loss_ratio*q_hat(:,t-1) + Y*(nabla(q_hat(:,t-1)) + GG ));
      %      q_hat(:,t) = q_hat(:,t-1) - alpha*(Y\(lambda_bar(:,t) - lambda_un(:,t) + power_loss_ratio*q_hat(:,t-1)) + (nabla(q_hat(:,t-1)) + GG ));
        else
            for iii=1:n
                comm_vector = zeros(n,1);
                i_neighbor = find(Y(iii,:)~=0); %neighboring buses of i
                for jjj=i_neighbor
                    if(jjj~=iii)
                        tau = randi(delay); % delayed value
                    else
                        tau=0;
                    end
                    delayed_t = max(t-tau,1);
                    delayed_t_minus = max(t-1-tau,1);
                    GG = max(min(xi(jjj,delayed_t) + c.*(q_hat(jjj,delayed_t_minus) - q_un(jjj)),0), xi(jjj,delayed_t)+c.*(q_hat(jjj,delayed_t_minus) - q_bar(jjj)));
                    comm_vector(jjj) = nabla_indvidual(q_hat(jjj,delayed_t_minus),jjj) + GG;
                end
                %GG = max(min(xi(:,t) + c*(q_hat(:,t-1) - q_un),0), xi(:,t)+c*(q_hat(:,t-1) - q_bar));
                %comm_vector = nabla(q_hat(:,t-1)) + GG );
                q_hat(iii,t) = q_hat(iii,t-1) - alpha.*(lambda_bar(iii,t) - lambda_un(iii,t) + power_loss_ratio*q_hat(iii,t-1) + Y(iii,:)*comm_vector );
            end
        end
   
       
    end
    %q_hat(:,t) = X*(lambda_un(:,t) - lambda_bar(:,t)) + xi_un(:,t) - xi_bar(:,t);
    q(:,t) = max(min(q_hat(:,t),q_bar),q_un); % ''actuall implemented reactive power''
    
    % ================ Linear Model for Voltage ====================
    % ================ Non-Linear Model for Voltage =================
    % total reactive power injection in all phases= q_inj that goes into OPENDSS
    % reactive power injection in controllbale nodes is given by  q, Here
    % qc=q
    % from previous equations, q(all)=G.Uc*qc
    q_inj=G.U_c*q(:,t); 
% q_inj=zeros(12,t);
    
    if control_flag==1
        [V_phase_pu] = OPENDSS_interface_qinj_static(t,load_var,q_inj,Data);
         
    end
    
    for h=1:length(V_phase_pu(:,1))
        v(h,t)=V_phase_pu(h,1)^2;
%         v_phase(h,t)=V_phase_pu(1,h);
    end

    for h=1:length(V_phase_pu(:,1))
        v_phase(h,t)=V_phase_pu(h,1);
    end
    %OpenDSS collects all phase voltages whereas we only need voltages for
    %control nodes
    % from prevous equations, vc=C*v(all)
    v_c(:,t)=G.C*v(:,t); % only squared control phase voltages  
    v_c_phase(:,t)=G.C*v_phase(:,t); % actual control phase voltages
    f(t) = f_func(q(:,t));
    fes(t) =  norm( [proj0(v_c(:,t)-v_bar); proj0(v_un-v_c(:,t)); proj0(q(:,t)-q_bar); proj0(q_un-q(:,t))]);

    
    

    
    
    if(t<T)
        % update for the multipliers
        for i=1:n
            if q_hat(i,t) + xi(i,t)/c(i)<q_un(i)
                xi(i,t+1) = xi(i,t) + beta(i)*(q_hat(i,t) - q_un(i));
            elseif q_hat(i,t) + xi(i,t)/c(i) > q_bar(i)
                xi(i,t+1) = xi(i,t) + beta(i)*(q_hat(i,t) - q_bar(i));
            else
                xi(i,t+1) = (1 - beta(i)/c(i))*xi(i,t);
            end
        end
        %xi_bar(:,t+1) = max(xi_bar(:,t) + beta * (q_hat(:,t) - q_bar), 0);
        %xi_un(:,t+1)  = max(xi_un(:,t) + beta * (q_un - q_hat(:,t)),0);
        
        if(noise_flag==1)
            v_measurement = v_c(:,max(t-5,1));
            measurement_noise_at_t = randn(n,1)*measurement_noise;
            v_measurement = (sqrt(v_measurement)+measurement_noise_at_t).^2;
        else
            v_measurement = v_c(:,t);
        end
            
        lambda_bar(:,t+1) = max(lambda_bar(:,t) + gamma.* (v_measurement - v_bar),0);
        lambda_un(:,t+1) = max(lambda_un(:,t) + gamma.*(v_un - v_measurement),0);
        
        
        % Output class
        var.v(:,t)=v(:,t);
        var.v_phase(:,t)=v_phase(:,t);
        var.v_c(:,t)=v_c(:,t);
        var.v_c_phase(:,t)=v_c_phase(:,t);
        var.q(:,t)=q(:,t);
        var.fes(t)=fes(t);
        var.f(t)=f(t);
        var.lambda_bar(:,t+1)=lambda_bar(:,t+1);
        var.lambda_un(:,t+1)=lambda_un(:,t+1);
        var.xi(:,t+1)=xi(:,t+1);
        var.q_hat(:,t)=q_hat(:,t);
        
    end
% end
%transpose
%V=v;
%Q=q;
%fes=fes;
%f=f;

end

