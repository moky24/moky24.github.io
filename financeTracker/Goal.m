classdef Goal
    %GOAL class
    %   represents a financial goal
    
    properties
        Amount
        Category
        Date
    end
    
    methods
        function obj = Goal(amount, category, date)
            %GOAL Construct an instance of this class
            %   Detailed explanation goes here
            obj.Amount = amount;
            obj.Category = category;
            obj.Date = date;
        end

    end
end

