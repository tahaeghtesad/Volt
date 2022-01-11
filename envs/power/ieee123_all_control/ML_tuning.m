clear all;
clc;


%network_model='123_bus_feeder';

%q_control='fixed' ; %1= all_control, 2=fixed control
Power_system_initialization
global v_un v_bar q_un q_bar a b power_loss_ratio Y measurement_noise delay  n delay_flag control_flag U_c C  T noise_flag load_var
delay_flag=0;
control_flag=1;
noise_flag=0;

measurement_noise=0;
delay=0;
%network_model='123_bus_feeder';

%Data_extraction
%Power_system_initialization(network_model)
var.q_hat = zeros(n,T); % ''virtual'' reactive power
var.xi = zeros(n,T); % lagrangian multiplier for reactive power constraint
var.lambda_bar = zeros(n,T); % lagrangian multipler for voltage constraint (upper limit)
var.lambda_un = zeros(n,T); % lagrangian multipler for voltage constraint (lower limit)
var.v_c = zeros(n,T); % voltage
var.v_c_phase = zeros(n,T); % voltage
var.q = zeros(n,T); % ''actual'' reactive power
var.f = zeros(1,T); % objective function value
var.fes = zeros(1,T); % feasibility of solution

% variables and constraints reuqired by the algorithm

% Parameters
v_un=Data.v_un_vec;
v_bar=Data.v_bar_vec;
q_un=Data.q_un_vec;
q_bar=Data.q_bar_vec;
a=Data.a;
b=Data.b;
power_loss_ratio=Data.power_loss_weight;
Y=G.Y_control;


% size of network
n = size(q_un,1); % number of controllable nodes
U_c=G.U_c;
% only for control nodes
v_un=G.C*v_un;
v_bar=G.C*v_bar;

C=G.C;
% loading
load_var=1;
% Algorithm parameters
for t=1:T
    
%............................HYPERPARAMETER INPUTS ..........................................................
% alpha = 10^(-3.7748424000032275)*ones(n,1); %0.001
% beta = 10^(-3.5788105351147337)*ones(n,1); %5
% gamma = 10^(3.7345339664082573)*ones(n,1); %200
% c=10^(1.3238327687752358)*ones(n,1); %1

alpha = 0.002*ones(n,1); %0.001
beta = 0.5*ones(n,1); %5
gamma = 100*ones(n,1); %200
c=1*ones(n,1); %1

%............................ALGORITHM STARTS ..........................................................

% projection functions
proj0 = @(r) max(r,zeros(size(r)));


% gradient handle
%X = inv(Y);
nabla = @(qqq) a.*qqq + b ;
nabla_indvidual = @(qqq,jjj) a(jjj)*qqq+b(jjj);
f_func = @(qqq) sum(1/2*a.*(qqq.^2) + b.*qqq);

%  if t==1
%         xi(:,t) =zeros(n,t); % for first iteration, xi=0
%         q_hat(:,t)=zeros(n,t); % for first iteration, q_hat=0
%         lambda_bar(:,t)=zeros(n,t);
%         lambda_un(:,t)=zeros(n,t);
%     else
%         q_hat(:,t-1)= var.q_hat(:,t-1) ; % ''virtual'' reactive power
%          xi(:,t)= var.xi(:,t) ; % lagrangian multiplier for reactive power constraint
%         lambda_bar(:,t)= var.lambda_bar(:,t) ; % lagrangian multipler for voltage constraint (upper limit)
%         lambda_un(:,t)= var.lambda_un(:,t)  ; % lagrangian multipler for voltage constraint (lower limit)
% %         var.v = zeros(n,T); % voltage
% %         var.q = zeros(n,T); % ''actual'' reactive power
% %         var.f = zeros(1,T); % objective function value
% %         var.fes = zeros(1,T); % feasibility of solution
%  end
    
  if(t>1)
        if(delay_flag==0)
            GG = max(min(var.xi(:,t) + c.*(var.q_hat(:,t-1) - q_un),0), var.xi(:,t)+c.*(var.q_hat(:,t-1) - q_bar));
            comm_vector = nabla(var.q_hat(:,t-1)) + GG ;
            var.q_hat(:,t) = var.q_hat(:,t-1) - alpha.*(var.lambda_bar(:,t) - var.lambda_un(:,t) + power_loss_ratio*var.q_hat(:,t-1) + Y*(nabla(var.q_hat(:,t-1)) + GG ));
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
                    GG = max(min(var.xi(jjj,delayed_t) + c(jjj)*(var.q_hat(jjj,delayed_t_minus) - q_un(jjj)),0), var.xi(jjj,delayed_t)+c(jjj)*(var.q_hat(jjj,delayed_t_minus) - q_bar(jjj)));
                    comm_vector(jjj) = nabla_indvidual(var.q_hat(jjj,delayed_t_minus),jjj) + GG;
                end
                %GG = max(min(xi(:,t) + c*(q_hat(:,t-1) - q_un),0), xi(:,t)+c*(q_hat(:,t-1) - q_bar));
                %comm_vector = nabla(q_hat(:,t-1)) + GG );
                var.q_hat(iii,t) = var.q_hat(iii,t-1) - alpha(iii)*(var.lambda_bar(iii,t) - var.lambda_un(iii,t) + power_loss_ratio*var.q_hat(iii,t-1) + Y(iii,:)*comm_vector );
            end
        end
   
       
  end
    
  q(:,t) = max(min(var.q_hat(:,t),q_bar),q_un); % ''actuall implemented reactive power''
   
   % from previous equations, q(all)=G.Uc*qc
    q_inj=U_c*q(:,t); 
% q_inj=zeros(12,t);
    
    if control_flag==1
        %[V_phase_pu] = OPENDSS_interface_qinj_static(t,load_var,q_inj,Data);
         [V_phase_pu] = pqinj_three_phase_static(Data,load_var,q_inj);
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
    v_c(:,t)=C*v(:,t); % only squared control phase voltages  
    v_c_phase(:,t)=C*v_phase(:,t); % actual control phase voltages
    f(t) = f_func(q(:,t));
    fes(t) =  norm( [proj0(v_c(:,t)-v_bar); proj0(v_un-v_c(:,t)); proj0(q(:,t)-q_bar); proj0(q_un-q(:,t))]);
 if(t<T)
        % update for the multipliers
        for i=1:n
            if var.q_hat(i,t) + var.xi(i,t)/c(i)<q_un(i)
                var.xi(i,t+1) = var.xi(i,t) + beta(i)*(var.q_hat(i,t) - q_un(i));
            elseif var.q_hat(i,t) + var.xi(i,t)/c(i) > q_bar(i)
                var.xi(i,t+1) = var.xi(i,t) + beta(i)*(var.q_hat(i,t) - q_bar(i));
            else
                var.xi(i,t+1) = (1 - beta(i)/c(i))*var.xi(i,t);
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
            
        var.lambda_bar(:,t+1) = max(var.lambda_bar(:,t) + gamma.* (v_measurement - v_bar),0);
        var.lambda_un(:,t+1) = max(var.lambda_un(:,t) + gamma.*(v_un - v_measurement),0);
        
        
        % Output class
%         var.v(:,t)=v(:,t);
%         var.v_phase(:,t)=v_phase(:,t);
        var.v_c(:,t)=v_c(:,t);
        var.v_c_phase(:,t)=v_c_phase(:,t);
        var.q(:,t)=q(:,t);
        var.fes(t)=fes(t);
        var.f(t)=f(t);
       
        
        
%        var.q_hat = zeros(n,T); % ''virtual'' reactive power
% var.xi = zeros(n,T); % lagrangian multiplier for reactive power constraint
% var.lambda_bar = zeros(n,T); % lagrangian multipler for voltage constraint (upper limit)
% var.lambda_un = zeros(n,T); % lagrangian multipler for voltage constraint (lower limit)
% var.v = zeros(n,T); % voltage
% var.q = zeros(n,T); % ''actual'' reactive power
% var.f = zeros(1,T); % objective function value
% var.fes = zeros(1,T); % feasibility of solution 
        
 end
    
 %............................ALGORITHM ENDS ..........................................................

end

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
    plot(m1,var.v_c_phase(:,1:T-1),'Linewidth',2);
    grid on;
    xlim([0 T]);
    xlabel('Iterations') ;
    ylabel('Bus voltages (pu)') ;
    %yticks([0.9 0.95 1.0 1.05]);
    %yticklabels({'0.9','0.95','1.0','1.05'});
    %legend({'V_{652} pu','q_{652} pu'},'Location','northeast');
    ax = gca;
    ax.FontSize = 16;



