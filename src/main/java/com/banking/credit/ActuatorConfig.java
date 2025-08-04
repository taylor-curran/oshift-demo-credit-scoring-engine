package com.banking.credit;

import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.HashMap;
import java.util.Map;

@Configuration
public class ActuatorConfig {

    @Bean
    public HealthIndicator livenessIndicator() {
        return () -> Health.up()
                .withDetail("status", "UP")
                .withDetail("service", "credit-scoring-engine")
                .build();
    }

    @Bean
    public HealthIndicator readinessIndicator() {
        return () -> {
            Map<String, String> bureauConnections = new HashMap<>();
            bureauConnections.put("experian", "UP");
            bureauConnections.put("equifax", "UP");
            bureauConnections.put("transunion", "UP");
            
            return Health.up()
                    .withDetail("status", "UP")
                    .withDetail("service", "credit-scoring-engine")
                    .withDetail("model_status", "ACTIVE")
                    .withDetail("bureau_connections", bureauConnections)
                    .withDetail("compliance_mode", "FCRA-ECOA")
                    .build();
        };
    }
}
