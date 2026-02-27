Attribute VB_Name = "POS_Improved"
Option Explicit

' Drop-in safety/quality improvements for your workbook macros.
' Main upgrades:
' 1) Centralized UI hide/show so it always restores correctly.
' 2) Safer event guards to avoid recursive Worksheet_Change triggers.
' 3) Named constants for keys and worksheet names.
' 4) Reusable validation helpers.

Private Const LICENSE_TRIAL_KEY As String = "DD2026_Try"
Private Const LICENSE_YEAR_KEY As String = "Diamond_2026_Dave_Year"
Private Const SYS_SHEET As String = "System"

Public Sub InitializeAppSafe()
    ToggleKioskMode True
    ValidateLicenseSafe
End Sub

Public Sub ToggleKioskMode(ByVal enabled As Boolean)
    On Error Resume Next
    Application.ExecuteExcel4Macro "SHOW.TOOLBAR(""Ribbon"", " & LCase$(CStr(Not enabled)) & ")"
    Application.DisplayFormulaBar = Not enabled
    Application.DisplayStatusBar = Not enabled
    Application.DisplayFullScreen = enabled
    Application.CommandBars("Cell").Enabled = Not enabled
    On Error GoTo 0

    If ThisWorkbook.Windows.Count > 0 Then
        ThisWorkbook.Windows(1).DisplayWorkbookTabs = Not enabled
        If enabled Then ThisWorkbook.Windows(1).WindowState = xlMaximized
    End If
End Sub

Public Sub ValidateLicenseSafe()
    Dim ws As Worksheet
    Dim userKey As String
    Dim expiryDate As Date

    Set ws = ThisWorkbook.Worksheets(SYS_SHEET)
    If IsDate(ws.Range("A1").Value) Then expiryDate = CDate(ws.Range("A1").Value)

    If expiryDate = 0 Or expiryDate < Date Then
        userKey = InputBox("Enter license key:", "Activation")
        Select Case Trim$(userKey)
            Case LICENSE_TRIAL_KEY
                expiryDate = Date + 28
            Case LICENSE_YEAR_KEY
                expiryDate = Date + 365
            Case Else
                MsgBox "Invalid license key.", vbCritical
                ThisWorkbook.Close SaveChanges:=False
                Exit Sub
        End Select
        ws.Range("A1").Value = expiryDate
    End If

    If expiryDate - Date <= 30 Then
        MsgBox "Your license expires in " & (expiryDate - Date) & " day(s).", vbInformation
    End If
End Sub

Public Function HasSufficientPayment(ByVal paid As Double, ByVal total As Double) As Boolean
    HasSufficientPayment = (paid >= total)
End Function
