
Power_system_initialization
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
Data.alpha = 0.001*ones(n,1);
Data.beta = 5*ones(n,1);
Data.gamma = 200*ones(n,1);
Data.c=1*ones(n,1);




% [v,v_phase,v_c,v_c_phase, q,fes,f,lambda_bar,lambda_un,xi,q_hat] = Input_parameter(Data,G,T,t);

[var] = optdist_vc_ML(T,Data,G,t,var);
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



