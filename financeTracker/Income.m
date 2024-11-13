classdef Income
    %INCOME class
    %   represents an income transaction
    
    properties
        Amount
        Category
        Date
    end
    
    methods
        % constructor function
        function obj = Income(amount, category, date)
            %INCOME Construct an instance of this class
            %   Detailed explanation goes here
            obj.Amount = amount;
            obj.Category = category;
            obj.Date = date;
        end
    end
end

