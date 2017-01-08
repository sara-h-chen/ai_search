% Solution of the traveling salesman problem by simulated annealing
% location of the cities
l = 10; d = l.ˆ2;
cities = zeros(d,2);
for k = 0:(d-1),
cities(k+1,:) = [fix(k/l) rem(k,l)]/l;
end
% distances between cities
dist = zeros(d);
for k1 = 1:d,
for k2 = 1:d,
dist(k1,k2) = norm(cities(k1,:)-cities(k2,:));
end
end
4
% Initial tour
tour = [1, 1+randperm(d-1), 1];
figure, plot(cities(:,1),cities(:,2),’*’), axis([-.1 1 -.1 1])
hold on
plot(cities(tour,1),cities(tour,2),’r’)
hold off
% Number of steps and cooling schedule
nsteps = 80;
Tinit = 5;
Tfinal = .01;
n = 1:nsteps;
T = Tinit*(Tfinal/Tinit).^(n/nsteps); % geometric schedule
% T = Tinit + (Tfinal-Tinit).*n/nsteps; % linear schedule
Length = zeros(1,nsteps+1);
Length(1) = LengthTour(tour,dist);
5
for n = 1:nsteps,
    % Pick two cities at random
    pair = randsample(2:d,2);
    i = min(pair); j = max(pair);
    % Replace segment
    new.tour = tour; new.tour(i:j) = tour(j:-1:i);
    
    % Compute length of new tour
    if rem(n,1000) == 0,
        new.length = LengthTour(new.tour,dist);
        Delta = new.length - Length(n);
    else
        Delta = dist(tour(i-1),tour(j)) + dist(tour(i),tour(j+1))
        - dist(tour(i-1),tour(i)) - dist(tour(j),tour(j+1));
        new.length = Length(n) + Delta;
    end

    % Decide whether or not to accept the new tour
    if rand(1) < min(exp(-Delta/T(n)),1),
        tour = new.tour;
        Length(n+1) = new.length;
    else
        Length(n+1) = Length(n);
    end
end


function Length = LengthTour(tour,dist)
% Calculate the length of a tour
Length = 0;
for k = 1:(length(tour)-1),
Length = Length + dist(tour(k),tour(k+1));
end