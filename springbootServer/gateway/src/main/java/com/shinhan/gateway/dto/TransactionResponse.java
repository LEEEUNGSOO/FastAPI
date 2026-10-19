package com.shinhan.gateway.dto;

import java.time.LocalDate;

// FastAPI Transaction 모델과 짝
public record TransactionResponse(String txId, LocalDate date, String category, Long amount) {}

/* ===== 전체 이해 =====
 * - 거래 한 건. 컨트롤러에서는 List<TransactionResponse> 로 받음
 * - "2026-10-29" 문자열을 Jackson이 LocalDate 로 바꿔 넣어 줌
 */