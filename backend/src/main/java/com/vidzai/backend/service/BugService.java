package com.vidzai.backend.service;

import com.vidzai.backend.model.BugReport;
import org.springframework.stereotype.Service;

@Service
public class BugService {

    public String processBug(BugReport bugReport) {

        return "Bug Received: " + bugReport.getBugReport();

    }
}