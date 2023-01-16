Recomb_1 = load('0.01Recomb.mat');
Recomb_10e10 = load('100000000Recomb.mat');

low_x = Recomb_1.lum.x0;
low_y = Recomb_1.lum.y0;

high_x = Recomb_10e10.lum.x0;
high_y = Recomb_10e10.lum.y0;


plot(low_x,low_y)
hold on
plot(high_x,high_y)