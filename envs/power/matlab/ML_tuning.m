
clc; close all;
T = 500;
Power_system_initialization
% Algorithm parameters
for t=1:T
alpha = 0.001*ones(n,1);
beta = 5*ones(n,1);
gamma = 200*ones(n,1);
c=1*ones(n,1);




% [v,v_phase,v_c,v_c_phase, q,fes,f,lambda_bar,lambda_un,xi,q_hat] = Input_parameter(Data,G,T,t);

[var] = step(alpha, beta, gamma, c, t);
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



