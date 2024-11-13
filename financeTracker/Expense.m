classdef Expense
    %EXPENSE class
    %   represents an expense transaction
    
    properties
        Amount
        Category
        Date
    end
    
    properties (Access = public)
        validCategories = {'food', 'bills', 'entertainment'}; % predefined categories 
    end

    methods
        % constructor function
        function obj = Expense(amount,category, date)
            %EXPENSE Construct an instance of this class
            %   Detailed explanation goes here
            if ismember(category, obj.validCategories) % if category is found in validCategories
                obj.Amount = amount;
                obj.Category = category;
                obj.Date = date;
            else
                error("invalid category");
            end
        end
    end
end

