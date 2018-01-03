function gen_samples= inverse_sampling(features,numsampl,disp)
if disp
 figure; histfit(features);
end
[Fi,xi] = ecdf(features);
if(disp)
 figure;
 stairs(xi,Fi,'r');
 xlabel('x'); ylabel('F(x)');
end
xj = xi(2:end);
Fj = (Fi(1:end-1)+Fi(2:end))/2;
if(disp)
    hold on
    plot(xj,Fj,'b.', xj,Fj,'b-');
    hold off
    legend({'ECDF' 'Breakpoints' 'Piecewise Linear Estimate'},'location','NW');
end

n=length(xj);
xj = [xj(1)-Fj(1)*(xj(2)-xj(1))/((Fj(2)-Fj(1)));
      xj;
      xj(n)+(1-Fj(n))*((xj(n)-xj(n-1))/(Fj(n)-Fj(n-1)))];
Fj = [0; Fj; 1];
if(disp)
    figure;
    hold on
    plot(xj,Fj,'b-','HandleVisibility','off');
    hold off
end


F = @(y) interp1(xj,Fj,y,'linear','extrap');
y = linspace(min(features),max(features),100);
if(disp)
    figure;
    plot(xj,Fj,'b-',y,F(y),'ko'); 
    xlabel('x'); 
    ylabel('F(x)');
    stairs(Fi,[xi(2:end); xi(end)],'r');
    hold on
    plot(Fj,xj,'b-');
    hold off
    ylabel('x'); xlabel('F(x)');
    legend({'ECDF' 'Piecewise Linear Estimate'},'location','NW');
end

Finv = @(u) interp1(Fj,xj,u,'linear','extrap');
u = rand(numsampl,1);
gen_samples=Finv(u);
if(disp)
    figure;
    hist(gen_samples,min(features(1,:)):0.25:max(features(1,:)));
    xlabel('x'); ylabel('Frequency');
end