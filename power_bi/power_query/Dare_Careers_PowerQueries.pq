// AWS_Cloud_Zoom_Attendance
let
    Source = Folder.Files("D:\AmaliTech\dare-careers-student-performance\data\raw\aws_cloud\Zoom Attendance"),
    #"Filtered Hidden Files1" = Table.SelectRows(Source, each [Attributes]?[Hidden]? <> true),
    #"Invoke Custom Function1" = Table.AddColumn(#"Filtered Hidden Files1", "Transform File", each #"Transform File"([Content])),
    #"Renamed Columns1" = Table.RenameColumns(#"Invoke Custom Function1", {"Name", "Source.Name"}),
    #"Removed Other Columns1" = Table.SelectColumns(#"Renamed Columns1", {"Source.Name", "Transform File"}),
    #"Expanded Table Column1" = Table.ExpandTableColumn(#"Removed Other Columns1", "Transform File", Table.ColumnNames(#"Transform File"(#"Sample File"))),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Table Column1",{{"Source.Name", type text}, {"Name", type text}, {"Email", type text}, {"Join Time", type time}, {"Leave Time", type time}, {"Duration", Int64.Type}, {"Role", type text}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type", "Attendance Date", each Date.FromText(
    Text.BeforeDelimiter([Source.Name], ".csv"),
    [Culture="en-US"]
)),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "Attendance Flag", each if [Duration] > #duration(0, 0, 30, 0)
then 1
else 0),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "Training Week", each "Week " & Text.From(
    Number.IntegerDivide(
        Duration.Days([Attendance Date] - #date(2024, 8, 5)),
        7
    ) + 1
)),
    #"Added Custom3" = Table.AddColumn(#"Added Custom2", "Track", each "AWS Cloud"),
    #"Added Custom4" = Table.AddColumn(#"Added Custom3", "Duration.1", each #duration(0, 0, [Duration], 0)),
    #"Removed Columns" = Table.RemoveColumns(#"Added Custom4",{"Duration"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"Duration.1", "Duration"}}),
    #"Filtered Rows" = Table.SelectRows(#"Renamed Columns", each true),
    #"Changed Type1" = Table.TransformColumnTypes(#"Filtered Rows",{{"Duration", type duration}}),
    #"Removed Columns1" = Table.RemoveColumns(#"Changed Type1",{"Attendance Flag"}),
    #"Added Custom5" = Table.AddColumn(#"Removed Columns1", "Attendance Flag", each if [Duration] > #duration(0, 0, 30, 0)
then 1
else 0)
in
    #"Added Custom5"

// Transform File
let
    Source = (Parameter1 as binary) => let
    Source = Csv.Document(Parameter1,[Delimiter=",", Columns=6, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true])
in
    #"Promoted Headers"
in
    Source

// Sample File
let
    Source = Folder.Files("D:\AmaliTech\dare-careers-student-performance\data\raw\aws_cloud\Zoom Attendance"),
    Navigation1 = Source{0}[Content]
in
    Navigation1

// PowerBI_Zoom_Attendance
let
    Source = Folder.Files("D:\AmaliTech\dare-careers-student-performance\data\raw\power_bi\Zoom Attendance"),
    #"Filtered Hidden Files1" = Table.SelectRows(Source, each [Attributes]?[Hidden]? <> true),
    #"Invoke Custom Function1" = Table.AddColumn(#"Filtered Hidden Files1", "Transform File", each #"Transform File"([Content])),
    #"Renamed Columns1" = Table.RenameColumns(#"Invoke Custom Function1", {"Name", "Source.Name"}),
    #"Removed Other Columns1" = Table.SelectColumns(#"Renamed Columns1", {"Source.Name", "Transform File"}),
    #"Expanded Table Column1" = Table.ExpandTableColumn(#"Removed Other Columns1", "Transform File", Table.ColumnNames(#"Transform File"(#"Sample File"))),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Table Column1",{{"Source.Name", type text}, {"Name", type text}, {"Email", type text}, {"Join Time", type time}, {"Leave Time", type time}, {"Duration", type duration}, {"Role", type text}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type", "Attendance Date", each Date.FromText(
    Text.BeforeDelimiter([Source.Name], ".csv"),
    [Culture="en-US"]
)),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "Attendance Flag", each if [Duration] > #duration(0, 0, 30, 0)
then 1
else 0),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "Training Week", each "Week " & Text.From(
    Number.IntegerDivide(
        Duration.Days([Attendance Date] - #date(2024, 8, 5)),
        7
    ) + 1
)),
    #"Added Custom3" = Table.AddColumn(#"Added Custom2", "Track", each "Power BI")
in
    #"Added Custom3"

// Fact_Zoom_Attendance
let
    Source = Table.Combine({AWS_Cloud_Zoom_Attendance, PowerBI_Zoom_Attendance}),
    #"Added Custom" = Table.AddColumn(Source, "LearnerTrackKey", each Text.Lower(Text.Trim([Email])) & "|" & [Track]),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom",{{"Attendance Date", type date}})
in
    #"Changed Type"

// AWS_Cloud_Participation
let
    Source = Excel.Workbook(File.Contents("D:\AmaliTech\dare-careers-student-performance\data\raw\aws_cloud\Participation\participation.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Participation",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date", type date}, {"Participants", type text}}),
    #"Split Column by Delimiter" = Table.ExpandListColumn(Table.TransformColumns(#"Changed Type", {{"Participants", Splitter.SplitTextByDelimiter(",", QuoteStyle.Csv), let itemType = (type nullable text) meta [Serialized.Text = true] in type {itemType}}}), "Participants"),
    #"Changed Type1" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"Participants", type text}}),
    #"Trimmed Text" = Table.TransformColumns(#"Changed Type1",{{"Participants", Text.Trim, type text}}),
    #"Added Custom" = Table.AddColumn(#"Trimmed Text", "Track", each "AWS Cloud")
in
    #"Added Custom"

// PowerBI_Participation
let
    Source = Excel.Workbook(File.Contents("D:\AmaliTech\dare-careers-student-performance\data\raw\power_bi\Participation\Participation records.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet1_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date", type date}, {"Participants", type text}}),
    #"Split Column by Delimiter" = Table.ExpandListColumn(Table.TransformColumns(#"Changed Type", {{"Participants", Splitter.SplitTextByDelimiter(",", QuoteStyle.Csv), let itemType = (type nullable text) meta [Serialized.Text = true] in type {itemType}}}), "Participants"),
    #"Changed Type1" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"Participants", type text}}),
    #"Trimmed Text" = Table.TransformColumns(#"Changed Type1",{{"Participants", Text.Trim, type text}}),
    #"Added Custom" = Table.AddColumn(#"Trimmed Text", "Track", each "Power BI")
in
    #"Added Custom"

// FactParticipation
let
    Source = Table.Combine({AWS_Cloud_Participation, PowerBI_Participation}),
    #"Merged Queries" = Table.NestedJoin(Source, {"Participants"}, LearnerNameMapping, {"Name"}, "LearnerNameMapping", JoinKind.LeftOuter),
    #"Expanded LearnerNameMapping" = Table.ExpandTableColumn(#"Merged Queries", "LearnerNameMapping", {"Email", "Track"}, {"Email", "Track.1"}),
    #"Removed Columns" = Table.RemoveColumns(#"Expanded LearnerNameMapping",{"Track.1"}),
    #"Added Custom" = Table.AddColumn(#"Removed Columns", "LearnerTrackKey", each Text.Lower(Text.Trim([Email])) & "|" & [Track])
in
    #"Added Custom"

// LearnerNameMapping
let
    Source = Fact_Zoom_Attendance,
    #"Removed Columns" = Table.RemoveColumns(Source,{"Source.Name", "Join Time", "Leave Time", "Duration", "Role", "Attendance Date", "Attendance Flag", "Training Week", "LearnerTrackKey"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns", {"Track", "Name"})
in
    #"Removed Duplicates"

// AWS_Cloud_Labs
let
    Source = Excel.Workbook(File.Contents("D:\AmaliTech\dare-careers-student-performance\data\raw\aws_cloud\Labs & Quizes\labs_and_quizzes.xlsx"), null, true),
    Labs_Sheet = Source{[Item="Labs",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Labs_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"email", type text}, {"Week 1", Int64.Type}, {"Week 2", Int64.Type}, {"Week 3", Int64.Type}, {"Week 4", Int64.Type}, {"Week 5", Int64.Type}, {"Week 6", Int64.Type}, {"Week 7", Int64.Type}, {"Week 8", Int64.Type}, {"Week 9", Int64.Type}, {"Week 10", Int64.Type}}),
    #"Unpivoted Other Columns" = Table.UnpivotOtherColumns(#"Changed Type", {"email"}, "Attribute", "Value"),
    #"Renamed Columns" = Table.RenameColumns(#"Unpivoted Other Columns",{{"Attribute", "Week"}, {"Value", "Score"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "Track", each "AWS Cloud")
in
    #"Added Custom"

// PowerBI_Labs
let
    Source = Excel.Workbook(File.Contents("D:\AmaliTech\dare-careers-student-performance\data\raw\power_bi\Labs & Quizes\Labs & Quizes.xlsx"), null, true),
    Labs_Sheet = Source{[Item="Labs",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Labs_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"email", type text}, {"Week 1", Int64.Type}, {"Week 2", Int64.Type}, {"Week 3", Int64.Type}, {"Week 4", Int64.Type}, {"Week 5", Int64.Type}, {"Week 6", Int64.Type}, {"Week 7", Int64.Type}, {"Week 8", Int64.Type}, {"Week 9", Int64.Type}, {"Week 10", Int64.Type}}),
    #"Unpivoted Other Columns" = Table.UnpivotOtherColumns(#"Changed Type", {"email"}, "Attribute", "Value"),
    #"Renamed Columns" = Table.RenameColumns(#"Unpivoted Other Columns",{{"Attribute", "Week"}, {"Value", "Score"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "Track", each "Power BI")
in
    #"Added Custom"

// PowerBI_Quizzes
let
    Source = Excel.Workbook(File.Contents("D:\AmaliTech\dare-careers-student-performance\data\raw\power_bi\Labs & Quizes\Labs & Quizes.xlsx"), null, true),
    Labs_Sheet = Source{[Item="Quizzes",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Labs_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"email", type text}, {"Week 1", Int64.Type}, {"Week 2", Int64.Type}, {"Week 3", Int64.Type}, {"Week 4", Int64.Type}, {"Week 5", Int64.Type}, {"Week 6", Int64.Type}, {"Week 7", Int64.Type}, {"Week 8", Int64.Type}, {"Week 9", Int64.Type}, {"Week 10", Int64.Type}}),
    #"Unpivoted Other Columns" = Table.UnpivotOtherColumns(#"Changed Type", {"email"}, "Attribute", "Value"),
    #"Renamed Columns" = Table.RenameColumns(#"Unpivoted Other Columns",{{"Attribute", "Week"}, {"Value", "Score"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "Track", each "Power BI")
in
    #"Added Custom"

// AWS_Cloud_Quizzes
let
    Source = Excel.Workbook(File.Contents("D:\AmaliTech\dare-careers-student-performance\data\raw\aws_cloud\Labs & Quizes\labs_and_quizzes.xlsx"), null, true),
    Labs_Sheet = Source{[Item="Quizzes",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Labs_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"email", type text}, {"Week 1", Int64.Type}, {"Week 2", Int64.Type}, {"Week 3", Int64.Type}, {"Week 4", Int64.Type}, {"Week 5", Int64.Type}, {"Week 6", Int64.Type}, {"Week 7", Int64.Type}, {"Week 8", Int64.Type}, {"Week 9", Int64.Type}, {"Week 10", Int64.Type}}),
    #"Unpivoted Other Columns" = Table.UnpivotOtherColumns(#"Changed Type", {"email"}, "Attribute", "Value"),
    #"Renamed Columns" = Table.RenameColumns(#"Unpivoted Other Columns",{{"Attribute", "Week"}, {"Value", "Score"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "Track", each "AWS Cloud")
in
    #"Added Custom"

// FactLabs
let
    Source = Table.Combine({AWS_Cloud_Labs, PowerBI_Labs}),
    #"Added Custom" = Table.AddColumn(Source, "LearnerTrackKey", each Text.Lower(Text.Trim([email])) & "|" & [Track])
in
    #"Added Custom"

// FactQuizzes
let
    Source = Table.Combine({AWS_Cloud_Quizzes, PowerBI_Quizzes}),
    #"Added Custom" = Table.AddColumn(Source, "LearnerTrackKey", each Text.Lower(Text.Trim([email])) & "|" & [Track])
in
    #"Added Custom"

// AWS_Cloud_Status
let
    Source = Excel.Workbook(File.Contents("D:\AmaliTech\dare-careers-student-performance\data\raw\aws_cloud\Status of Learners\participant_status.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Sheet1_Sheet,{{"Column1", type text}, {"Column2", type text}, {"Column3", type text}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type", "Track", each "AWS Cloud"),
    #"Promoted Headers" = Table.PromoteHeaders(#"Added Custom", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers",{{"email", type text}, {"Graduation Status", type text}, {"Certification Status", type text}, {"AWS Cloud", type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type1",{{"AWS Cloud", "Track"}})
in
    #"Renamed Columns"

// PowerBI_Status
let
    Source = Excel.Workbook(File.Contents("D:\AmaliTech\dare-careers-student-performance\data\raw\power_bi\Status of Learners\Status of Participanat.xlsx"), null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(Sheet1_Sheet,{{"Column1", type text}, {"Column2", type text}, {"Column3", type text}}),
    #"Promoted Headers" = Table.PromoteHeaders(#"Changed Type", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers",{{"email", type text}, {"Graduation Status", type text}, {"Certification Status", type text}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type1", "Track", each "Power BI")
in
    #"Added Custom"

// FactLearnerStatus
let
    Source = Table.Combine({AWS_Cloud_Status, PowerBI_Status}),
    #"Added Custom" = Table.AddColumn(Source, "LearnerTrackKey", each Text.Lower(Text.Trim([email])) & "|" & [Track])
in
    #"Added Custom"

// DimLearner
let
    Source = FactLearnerStatus,
    #"Removed Columns" = Table.RemoveColumns(Source,{"Graduation Status", "Certification Status"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns", {"LearnerTrackKey"}),
    #"Merged Queries" = Table.NestedJoin(#"Removed Duplicates", {"LearnerTrackKey"}, FactLearnerStatus, {"LearnerTrackKey"}, "FactLearnerStatus", JoinKind.LeftOuter),
    #"Expanded FactLearnerStatus" = Table.ExpandTableColumn(#"Merged Queries", "FactLearnerStatus", {"Graduation Status", "Certification Status"}, {"FactLearnerStatus.Graduation Status", "FactLearnerStatus.Certification Status"}),
    #"Added Custom" = Table.AddColumn(#"Expanded FactLearnerStatus", "Cohort", each "Cohort 1"),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "Certification Type", each if [Track] = "AWS Cloud" then "AWS"
else if [Track] = "Power BI" then "Power BI"
else null),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom1",{{"Certification Type", type text}})
in
    #"Changed Type"

// DimDate
let
    Source = Fact_Zoom_Attendance,
    #"Removed Columns" = Table.RemoveColumns(Source,{"Source.Name", "Name", "Email", "Join Time", "Leave Time", "Duration", "Role", "Attendance Flag", "Training Week", "Track", "LearnerTrackKey"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"Attendance Date", "Date"}}),
    #"Removed Duplicates" = Table.Distinct(#"Renamed Columns"),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Duplicates",{{"Date", type date}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type", "Training Week", each "Week " & Text.From(
    Number.IntegerDivide(
        Duration.Days([Date] - #date(2024, 8, 5)),
        7
    ) + 1
)),
    #"Inserted Year" = Table.AddColumn(#"Added Custom", "Year", each Date.Year([Date]), Int64.Type),
    #"Inserted Month" = Table.AddColumn(#"Inserted Year", "Month", each Date.Month([Date]), Int64.Type),
    #"Inserted Month Name" = Table.AddColumn(#"Inserted Month", "Month Name", each Date.MonthName([Date]), type text),
    #"Removed Columns1" = Table.RemoveColumns(#"Inserted Month Name",{"Month"}),
    #"Inserted Day" = Table.AddColumn(#"Removed Columns1", "Day", each Date.Day([Date]), Int64.Type)
in
    #"Inserted Day"

// DimWeek
let
    Source = FactLabs,
    #"Removed Columns" = Table.RemoveColumns(Source,{"email", "Score", "Track", "LearnerTrackKey"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns"),
    #"Added Custom" = Table.AddColumn(#"Removed Duplicates", "Week Number", each Number.FromText(Text.AfterDelimiter([Week], " ")))
in
    #"Added Custom"

// DAX_Measures
let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlSKjQUA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Placeholder = _t]),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Placeholder", Int64.Type}})
in
    #"Changed Type"